import os
import re
import json
from typing import List, Dict, Tuple, Set
from pypdf import PdfReader
from neo4j import GraphDatabase
from preprocess_pdfs import read_pdfs_from_directory
from rich.console import Console
from tqdm import tqdm
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()
CACHE_FILE = "processed_docs_cache.json"

def get_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    # Normalize path for consistent comparison
    file_path = os.path.normpath(file_path)
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read the file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_cache() -> Dict:
    """Load processed documents from cache"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load cache file: {str(e)}[/yellow]")
    return {}

def save_cache(cache: Dict):
    """Save processed documents to cache"""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not save cache file: {str(e)}[/yellow]")

class ThreeGPPEntityExtractor:
    def __init__(self):
        # Core regex patterns for 3GPP NAS domain
        self.patterns = {
            "NETWORK_ELEMENT": [
                # Core Network Elements
                r'\b(?:UE|AMF|SMF|UDM|AUSF|SEAF|MME|gNB|ng-eNB)\b',
                r'\b(?:Access and Mobility Management Function|Session Management Function)\b',
                r'\b(?:User Equipment|Authentication Server Function|Security Anchor Function)\b',
                r'\b(?:Next Generation Node B|Next Generation eNodeB)\b'
            ],
            "PROCEDURE": [
                # Main NAS Procedures
                r'\b(?:Initial|Mobility|Periodic|Emergency)\s+Registration\s+Procedure\b',
                r'\b(?:UE|Network)-initiated\s+De-registration\s+Procedure\b',
                r'\b(?:Service\s+Request|PDU\s+Session\s+Establishment)\s+Procedure\b',
                # Sub-procedures
                r'\b(?:Authentication|Security Mode Control|Identity)\s+Procedure\b',
                r'\b(?:UE Configuration Update|QoS Flow Establishment)\s+Procedure\b',
                r'\b(?:PDU Session Resource Setup|Service Accept|Service Reject)\s+Procedure\b',
                # Generic Procedure Patterns
                r'\b(?:5GMM|EMM)\s+(?:Specific|Common)\s+Procedure\b',
                r'\b(?:NAS Transport|Handover)\s+Procedure\b'
            ],
            "PROCEDURE_RELATIONSHIP": [
                # Sub-procedure relationships
                r'as\s+part\s+of\s+(?:the\s+)?([A-Za-z\s]+(?:Procedure|procedure))',
                r'during\s+(?:the\s+)?([A-Za-z\s]+(?:Procedure|procedure))',
                r'initiated\s+by\s+(?:the\s+)?([A-Za-z\s]+(?:Procedure|procedure))',
                r'required\s+for\s+(?:the\s+)?([A-Za-z\s]+(?:Procedure|procedure))'
            ],
            "SPECIFICATION_REFERENCE": [
                # Section references
                r'(?:section|clause)\s+(\d+\.\d+\.\d+(?:\.\d+)?)',
                r'TS\s+24\.501\s+(?:section|clause)?\s*(\d+\.\d+\.\d+(?:\.\d+)?)',
                r'3GPP\s+TS\s+24\.501\s+(?:section|clause)?\s*(\d+\.\d+\.\d+(?:\.\d+)?)'
            ],
            "MESSAGE": [
                # NAS Messages
                r'\b(?:Authentication|Identity|Security Mode)\s+(?:Request|Response|Command|Result|Complete)\b',
                r'\b(?:Registration|Deregistration)\s+(?:Request|Accept|Reject|Complete)\b',
                r'\b(?:Service|Configuration|Status)\s+(?:Request|Accept|Reject|Notification)\b',
                r'\b(?:PDU Session|Bearer Resource|NAS)\s+(?:Establishment|Modification|Release)\s+(?:Request|Accept|Reject)\b'
            ],
            "STATE": [
                # UE and Network States
                r'\b(?:CM|RM|EMM|MM|RRC)-(?:IDLE|CONNECTED|REGISTERED|DEREGISTERED)\b',
                r'\b(?:5GMM|EMM)-(?:IDLE|CONNECTED|REGISTERED|DEREGISTERED)\b',
                r'\b(?:REGISTERED|DEREGISTERED|IDLE|CONNECTED)\s+(?:State|Mode)\b'
            ]
        }
        
        # Compile all patterns
        self.compiled_patterns = {
            entity_type: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for entity_type, patterns in self.patterns.items()
        }

        # Known procedure relationships from multiple 3GPP specifications
        self.known_procedures = {
            # TS 24.501 (5G NAS) Procedures
            "Initial Registration Procedure": {
                "section": "5.5.1.2",
                "specification": "TS 24.501",
                "description": "Register a UE with the network for 5GS services",
                "sub_procedures": [
                    ("Authentication Procedure", "5.4.1", "Primary and secondary authentication of the UE"),
                    ("Security Mode Control Procedure", "5.4.2", "Activate NAS security between UE and network"),
                    ("UE Configuration Update Procedure", "5.4.4", "Update UE configuration information")
                ]
            },
            "Mobility Registration Procedure": {
                "section": "5.5.1.3",
                "specification": "TS 24.501",
                "description": "Handle mobility and periodic updates",
                "sub_procedures": [
                    ("Authentication Procedure", "5.4.1", "Re-authentication during mobility"),
                    ("Security Mode Control Procedure", "5.4.2", "Security context handling during mobility")
                ]
            },
            "Deregistration Procedure": {
                "section": "5.5.2",
                "specification": "TS 24.501",
                "description": "Detach UE from the network",
                "sub_procedures": [
                    ("UE-initiated Deregistration Procedure", "5.5.2.2", "UE requests to deregister from network"),
                    ("Network-initiated Deregistration Procedure", "5.5.2.3", "Network requests UE to deregister")
                ]
            },
            "Service Request Procedure": {
                "section": "5.6.1",
                "specification": "TS 24.501",
                "description": "Request services from the network in CM-IDLE state",
                "sub_procedures": [
                    ("Service Accept Procedure", "5.6.1.4", "Network accepts the service request"),
                    ("Service Reject Procedure", "5.6.1.5", "Network rejects the service request"),
                    ("Authentication Procedure", "5.4.1.3", "Authentication during service request")
                ]
            },
            "PDU Session Establishment": {
                "section": "6.4.1",
                "specification": "TS 24.501",
                "description": "Establish data connectivity through PDU session",
                "sub_procedures": [
                    ("PDU Session Authentication Procedure", "6.4.1.2", "Authenticate PDU session establishment request"),
                    ("QoS Flow Establishment Procedure", "6.4.1.3", "Set up quality of service flows"),
                    ("PDU Session Resource Setup Procedure", "6.4.1.4", "Allocate network resources")
                ]
            },
            
            # TS 24.301 (EPS NAS) Procedures
            "EPS Attach Procedure": {
                "section": "5.5.1",
                "specification": "TS 24.301",
                "description": "Register a UE with the network for EPS services",
                "sub_procedures": [
                    ("EPS Authentication Procedure", "5.4.2", "Authentication and key agreement"),
                    ("EPS Security Mode Control", "5.4.3", "Activate NAS security"),
                    ("ESM Default Bearer Setup", "6.4.1", "Establish default EPS bearer")
                ]
            },
            "EPS Tracking Area Update": {
                "section": "5.5.3",
                "specification": "TS 24.301",
                "description": "Update UE location and registration in EPS",
                "sub_procedures": [
                    ("EPS Authentication Procedure", "5.4.2", "Re-authentication during TAU"),
                    ("EPS Security Mode Control", "5.4.3", "Security context update during TAU")
                ]
            },
            "EPS Detach Procedure": {
                "section": "5.5.2",
                "specification": "TS 24.301",
                "description": "Detach UE from EPS network",
                "sub_procedures": [
                    ("UE-initiated Detach", "5.5.2.2", "UE requests to detach from network"),
                    ("Network-initiated Detach", "5.5.2.3", "Network requests UE to detach")
                ]
            },
            
            # Cross-specification Procedures (Interworking)
            "5GS to EPS Handover": {
                "section": "4.11.2",
                "specification": "TS 24.501",
                "related_spec": "TS 24.301",
                "description": "Handover from 5GS to EPS network",
                "sub_procedures": [
                    ("TAU Procedure", "5.5.3", "Registration in target EPS network"),
                    ("EPS Bearer Context Setup", "6.4.1", "Setup EPS bearers for handed over PDU sessions")
                ]
            },
            "EPS to 5GS Handover": {
                "section": "4.11.2",
                "specification": "TS 24.301",
                "related_spec": "TS 24.501",
                "description": "Handover from EPS to 5GS network",
                "sub_procedures": [
                    ("Registration Procedure", "5.5.1.2", "Registration in target 5GS network"),
                    ("PDU Session Establishment", "6.4.1", "Convert EPS bearers to PDU sessions")
                ]
            }
        }

    def extract_entities(self, text: str) -> Set[Tuple[str, str]]:
        """Extract entities using regex patterns"""
        entities = set()
        
        # Apply each pattern and collect entities
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    entity_text = match.group().strip()
                    # Normalize entity text to handle case variations
                    if entity_type in ["NETWORK_ELEMENT", "PROTOCOL", "STATE"]:
                        entity_text = entity_text.upper()
                    else:
                        entity_text = entity_text.title()
                    entities.add((entity_text, entity_type))
        
        return entities

    def _extract_properties(self, sentence: str) -> Dict:
        """Extract properties like parameters, conditions, and timing from text"""
        properties = {
            "parameters": [],
            "conditions": [],
            "timing": []
        }
        
        for prop_type, patterns in self.property_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    if match.groups():
                        properties[prop_type].append(match.group(1).strip())
        
        return {k: v for k, v in properties.items() if v}  # Remove empty properties

    def _determine_relationship(self, sentence: str, entity1: str, type1: str, entity2: str, type2: str) -> Tuple[str, Dict]:
        """Determine relationships and their properties based on 3GPP NAS domain knowledge"""
        sentence = sentence.lower()
        entity1_lower = entity1.lower()
        entity2_lower = entity2.lower()
        
        # Extract properties for the relationship
        properties = self._extract_properties(sentence)
        
        # Core relationship patterns
        patterns = {
            'sends': r'(?:sends?|transmits?|forwards?)',
            'receives': r'(?:receives?|accepts?|processes?)',
            'initiates': r'(?:initiates?|triggers?|starts?)',
            'performs': r'(?:performs?|executes?|carries? out)',
            'uses': r'(?:uses?|utilizes?|employs?)',
            'defines': r'(?:defines?|specifies?|describes?)',
            'transitions': r'(?:transitions?|changes?|moves?) to',
            'results': r'(?:results? in|leads? to|causes?)',
            'communicates': r'(?:communicates?|interacts?|exchanges?) with',
            'authenticates': r'(?:authenticates?|verifies?|validates?)',
            'triggers': r'(?:triggers?|causes?|leads? to)',
            'depends_on': r'(?:depends? on|requires?|needs?)',
            'precedes': r'(?:precedes?|comes? before|happens? before)',
            'follows': r'(?:follows?|comes? after|happens? after)',
            'handles': r'(?:handles?|processes?|manages?)',
            'interrupts': r'(?:interrupts?|stops?|halts?)',
            'processes': r'(?:processes?|handles?|manages?)'
        }
        
        # Relationship mapping based on entity types
        if type1 == "PROCEDURE" and type2 == "MESSAGE":
            if re.search(f"{entity1_lower}.*{patterns['uses']}.*{entity2_lower}", sentence):
                return "USES_MESSAGE", properties
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "PROCEDURE":
            if re.search(f"{entity1_lower}.*{patterns['initiates']}.*{entity2_lower}", sentence):
                return "INITIATES", properties
            if re.search(f"{entity1_lower}.*{patterns['performs']}.*{entity2_lower}", sentence):
                return "PERFORMS", properties
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "MESSAGE":
            if re.search(f"{entity1_lower}.*{patterns['sends']}.*{entity2_lower}", sentence):
                return "SENDS", properties
            if re.search(f"{entity1_lower}.*{patterns['receives']}.*{entity2_lower}", sentence):
                return "RECEIVES", properties
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "NETWORK_ELEMENT":
            if re.search(f"{entity1_lower}.*{patterns['communicates']}.*{entity2_lower}", sentence):
                return "COMMUNICATES_WITH", properties
            if re.search(f"{entity1_lower}.*{patterns['authenticates']}.*{entity2_lower}", sentence):
                return "AUTHENTICATES", properties
            
        elif type1 == "PROTOCOL" and type2 in ["MESSAGE", "PROCEDURE"]:
            if re.search(f"{entity1_lower}.*{patterns['defines']}.*{entity2_lower}", sentence):
                return "DEFINES", properties
            if re.search(f"{entity1_lower}.*{patterns['uses']}.*{entity2_lower}", sentence):
                return "USES", properties
            
        elif type1 == "STATE" and type2 == "PROCEDURE":
            if re.search(f"{entity2_lower}.*{patterns['results']}.*{entity1_lower}", sentence):
                return "RESULTS_IN", properties
                
        elif type1 == "SPECIFICATION" and type2 in ["PROCEDURE", "MESSAGE"]:
            if re.search(f"{entity1_lower}.*{patterns['defines']}.*{entity2_lower}", sentence):
                return "DEFINES", properties
                
        elif type1 == "STATE" and type2 == "STATE":
            if re.search(f"{patterns['transitions']}.*{entity2_lower}", sentence):
                return "TRANSITIONS_TO", properties
                
        elif type1 == "ACTION" and type2 == "EVENT":
            if re.search(f"{entity1_lower}.*{patterns['triggers']}.*{entity2_lower}", sentence):
                return "TRIGGERS", properties
            if re.search(f"{entity1_lower}.*{patterns['handles']}.*{entity2_lower}", sentence):
                return "HANDLES", properties
                
        elif type1 == "EVENT" and type2 == "ACTION":
            if re.search(f"{entity1_lower}.*{patterns['triggers']}.*{entity2_lower}", sentence):
                return "TRIGGERS", properties
                
        elif type1 == "ACTION" and type2 == "STATE":
            if re.search(f"{entity1_lower}.*{patterns['results']}.*{entity2_lower}", sentence):
                return "RESULTS_IN", properties
                
        elif type1 == "EVENT" and type2 == "PROCEDURE":
            if re.search(f"{entity1_lower}.*{patterns['triggers']}.*{entity2_lower}", sentence):
                return "TRIGGERS", properties
            if re.search(f"{entity1_lower}.*{patterns['interrupts']}.*{entity2_lower}", sentence):
                return "INTERRUPTS", properties
                
        elif type1 == "ACTION" and type2 == "MESSAGE":
            if re.search(f"{entity1_lower}.*{patterns['sends']}.*{entity2_lower}", sentence):
                return "SENDS", properties
            if re.search(f"{entity1_lower}.*{patterns['processes']}.*{entity2_lower}", sentence):
                return "PROCESSES", properties
        
        return None, {}

    def extract_relationships(self, text: str, entities: Set[Tuple[str, str]]) -> List[Tuple[str, str, str, Dict]]:
        """Extract relationships with properties between entities"""
        relationships = []
        sentences = [s.strip() for s in re.split(r'[.!?]+(?=(?:[A-Z]|\s|$))', text) if s.strip()]
        entity_dict = {entity[0].lower(): (entity[0], entity[1]) for entity in entities}
        
        for sentence in sentences:
            sentence = sentence.lower().strip()
            found_entities = []
            
            for entity_text in entity_dict:
                if entity_text in sentence:
                    found_entities.append(entity_dict[entity_text])
            
            for i in range(len(found_entities)):
                for j in range(i + 1, len(found_entities)):
                    entity1, type1 = found_entities[i]
                    entity2, type2 = found_entities[j]
                    
                    relationship, properties = self._determine_relationship(
                        sentence, entity1, type1, entity2, type2
                    )
                    if relationship:
                        relationships.append((entity1, entity2, relationship, properties))
        
        return relationships

    def extract_procedure_relationships(self, text: str) -> List[Dict]:
        """Extract procedure relationships with their specifications"""
        relationships = []
        
        # First pass: identify main procedures
        for proc_name, proc_info in self.known_procedures.items():
            if re.search(rf'\b{re.escape(proc_name)}\b', text, re.IGNORECASE):
                proc_data = {
                    "name": proc_name,
                    "type": "MAIN_PROCEDURE",
                    "section": proc_info["section"],
                    "specification": proc_info["specification"],
                    "description": proc_info["description"],
                    "sub_procedures": []
                }
                
                # Add related specification if it exists
                if "related_spec" in proc_info:
                    proc_data["related_specification"] = proc_info["related_spec"]
                
                # Second pass: identify sub-procedures for this main procedure
                for sub_proc in proc_info["sub_procedures"]:
                    name, section, description = sub_proc
                    if re.search(rf'\b{re.escape(name)}\b', text, re.IGNORECASE):
                        proc_data["sub_procedures"].append({
                            "name": name,
                            "type": "SUB_PROCEDURE",
                            "section": section,
                            "description": description
                        })
                
                relationships.append(proc_data)
        
        return relationships

def process_documents(documents: List[Dict[str, str]]) -> List[Dict]:
    """Process documents to extract entities and relationships with properties"""
    extractor = ThreeGPPEntityExtractor()
    processed_docs = []
    
    for doc in documents:
        text = doc['text']
        
        # Extract all entities
        entities = extractor.extract_entities(text)
        
        # Extract procedure relationships
        procedures = extractor.extract_procedure_relationships(text)
        
        # Process the document
        processed_doc = {
            'source': doc.get('source', 'Unknown'),
            'entities': [{'text': entity[0], 'type': entity[1]} for entity in entities],
            'procedures': procedures,
            'relationships': []  # We'll focus on procedure relationships for now
        }
        
        processed_docs.append(processed_doc)
    
    return processed_docs

def store_procedures_in_neo4j(driver, procedures: List[Dict]):
    """Store procedures and their relationships in Neo4j"""
    with driver.session() as session:
        for proc in procedures:
            # Create main procedure node with specification info
            session.run("""
                MERGE (p:Procedure {name: $name})
                SET p.type = $type,
                    p.section = $section,
                    p.specification = $specification,
                    p.description = $description
            """, name=proc['name'], type=proc['type'], 
                 section=proc['section'], 
                 specification=proc['specification'],
                 description=proc['description'])
            
            # Add related specification if it exists
            if 'related_specification' in proc:
                session.run("""
                    MATCH (p:Procedure {name: $name})
                    MERGE (s:Specification {name: $spec_name})
                    MERGE (p)-[:RELATED_TO_SPEC]->(s)
                """, name=proc['name'], spec_name=proc['related_specification'])
            
            # Create sub-procedure nodes and relationships
            for sub in proc.get('sub_procedures', []):
                session.run("""
                    MERGE (p:Procedure {name: $main_name})
                    MERGE (s:Procedure {name: $sub_name})
                    SET s.type = $type,
                        s.section = $section,
                        s.description = $description
                    MERGE (p)-[:HAS_SUB_PROCEDURE]->(s)
                """, main_name=proc['name'], 
                     sub_name=sub['name'],
                     type=sub['type'], 
                     section=sub['section'],
                     description=sub['description'])

def extract_and_store_procedures(pdf_dir: str, neo4j_driver) -> None:
    """Extract procedures from PDFs and store them in Neo4j"""
    # Read PDFs
    documents = read_pdfs_from_directory(pdf_dir)
    
    # Process documents
    processed_docs = process_documents(documents)
    
    # Extract all procedures
    all_procedures = []
    for doc in processed_docs:
        all_procedures.extend(doc.get('procedures', []))
    
    # Store in Neo4j
    store_procedures_in_neo4j(neo4j_driver, all_procedures)
    
    return all_procedures

# Usage Example
if __name__ == "__main__":
    DATA_DIR = "data"
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    
    if not NEO4J_PASSWORD:
        console.print("[red]❌ Error: NEO4J_PASSWORD environment variable must be set[/red]")
        exit(1)
    
    try:
        console.print("[blue]🔍 Reading and preprocessing 3GPP documents...[/blue]")
        documents = read_pdfs_from_directory(DATA_DIR)
        
        if not documents:
            console.print("[red]❌ No documents were found or successfully preprocessed.[/red]")
            exit(1)
            
        console.print(f"[green]✅ Successfully preprocessed {len(documents)} documents.[/green]")
        
        console.print("[blue]🔍 Extracting entities and relationships...[/blue]")
        processed_docs = process_documents(documents)
        
        if not processed_docs:
            console.print("[red]❌ No documents were successfully processed.[/red]")
            exit(1)
            
        console.print(f"[green]✅ Successfully processed {len(processed_docs)} documents.[/green]")
        console.print("[blue]💾 Storing data in Neo4j...[/blue]")
        
        # Create Neo4j driver
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        
        # Extract all procedures from processed documents
        all_procedures = []
        for doc in processed_docs:
            all_procedures.extend(doc.get('procedures', []))
        
        # Store procedures in Neo4j
        store_procedures_in_neo4j(driver, all_procedures)
        
        console.print("[green]✅ Successfully stored data in Neo4j![/green]")
        
        # Close Neo4j driver
        driver.close()
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        exit(1)
