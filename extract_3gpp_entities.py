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
                # NAS Procedures
                r'\b(?:Initial|Service|Periodic|Emergency|Normal)\s+(?:Registration|Attach)\b',
                r'\b(?:Authentication|Security Mode Control|Identity)\s+(?:Procedure)\b',
                r'\b(?:NAS Transport|PDU Session Establishment)\s+(?:Procedure)\b',
                r'\b(?:Handover|De-registration|Service Request)\s+(?:Procedure)\b',
                r'\b(?:5GMM|EMM)\s+(?:Specific Procedure|Common Procedure)\b'
            ],
            "MESSAGE": [
                # NAS Messages
                r'\b(?:Authentication|Identity|Security Mode)\s+(?:Request|Response|Command|Result|Complete)\b',
                r'\b(?:Registration|Deregistration)\s+(?:Request|Accept|Reject|Complete)\b',
                r'\b(?:Service|Configuration|Status)\s+(?:Request|Accept|Reject|Notification)\b',
                r'\b(?:PDU Session|Bearer Resource|NAS)\s+(?:Establishment|Modification|Release)\s+(?:Request|Accept|Reject)\b'
            ],
            "PROTOCOL": [
                # Protocol Types
                r'\b(?:NAS|RRC|NGAP|S1AP)\s+(?:Protocol|Signalling|Layer)\b',
                r'\b(?:5G|LTE)\s+(?:NAS|RRC)\b',
                r'\b(?:N1|N2|N11|N12)\s+(?:Interface|Protocol)\b'
            ],
            "STATE": [
                # UE and Network States
                r'\b(?:CM|RM|EMM|MM|RRC)-(?:IDLE|CONNECTED|REGISTERED|DEREGISTERED)\b',
                r'\b(?:5GMM|EMM)-(?:IDLE|CONNECTED|REGISTERED|DEREGISTERED)\b',
                r'\b(?:REGISTERED|DEREGISTERED|IDLE|CONNECTED)\s+(?:State|Mode)\b'
            ],
            "SPECIFICATION": [
                # 3GPP Specifications
                r'(?:3GPP\s+)?TS\s+\d+\.\d+(?:\.\d+)?',
                r'3GPP\s+(?:TS|TR)\s+\d+\.\d+(?:\.\d+)?',
                r'Release\s+(?:1[5-9]|20)',
                r'Rel-(?:1[5-9]|20)'
            ],
            "ACTION": [
                # NAS Actions
                r'\b(?:Start|Stop|Initiate|Release|Establish|Modify)\s+(?:Timer|Connection|Session|Bearer)\b',
                r'\b(?:Send|Receive|Forward|Process)\s+(?:Message|Request|Response)\b',
                r'\b(?:Verify|Check|Validate)\s+(?:Identity|Security|Integrity|MAC)\b',
                r'\b(?:Generate|Derive|Calculate)\s+(?:Key|Token|Parameter|Value)\b',
                r'\b(?:Allocate|Assign|Reserve)\s+(?:Resource|Address|Identity)\b'
            ],
            "EVENT": [
                # NAS Events
                r'\b(?:Timer)\s+(?:Expiry|Timeout|Start|Stop)\b',
                r'\b(?:Authentication|Security)\s+(?:Success|Failure|Error)\b',
                r'\b(?:Connection|Session|Bearer)\s+(?:Setup|Release|Loss)\b',
                r'\b(?:Registration|Service)\s+(?:Accept|Reject|Success|Failure)\b',
                r'\b(?:Radio|Link)\s+(?:Failure|Recovery|Error)\b'
            ]
        }
        
        # Compile all patterns
        self.compiled_patterns = {
            entity_type: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for entity_type, patterns in self.patterns.items()
        }

        # Properties patterns for metadata extraction
        self.property_patterns = {
            "parameters": [
                r'(?:with|using)\s+parameter[s]?\s+([^.]+)',
                r'parameter[s]?\s+(?:include|are)\s+([^.]+)',
                r'(?:value|setting)\s+(?:of|for)\s+([^.]+)'
            ],
            "conditions": [
                r'(?:if|when|unless)\s+([^,]+)',
                r'(?:provided|assuming)\s+that\s+([^,]+)',
                r'(?:in case|in the event)\s+(?:of|that)\s+([^.]+)'
            ],
            "timing": [
                r'(?:after|before|during|within)\s+([^,]+)',
                r'(?:timeout|expiry)\s+of\s+([^.]+)',
                r'(?:timer|counter)\s+(?:T\d+|N\d+)'
            ]
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

def process_documents(documents: List[Dict[str, str]]) -> List[Dict]:
    """Process documents to extract entities and relationships with properties"""
    processed_docs = []
    cache = load_cache()
    extractor = ThreeGPPEntityExtractor()
    
    for doc in documents:
        file_path = doc["metadata"]["file_path"]
        file_hash = get_file_hash(file_path)
        
        if file_path in cache and cache[file_path]["hash"] == file_hash:
            console.print(f"[green]Using cached results for {file_path}[/green]")
            processed_docs.append(cache[file_path]["data"])
            continue
            
        console.print(f"[blue]Processing {file_path}[/blue]")
        text = doc["text"]
        
        entities = extractor.extract_entities(text)
        relationships = extractor.extract_relationships(text, entities)
        
        processed_doc = {
            "entities": list(entities),
            "relationships": list(relationships),  # Now includes properties
            "metadata": doc["metadata"]
        }
        
        cache[file_path] = {
            "hash": file_hash,
            "data": processed_doc
        }
        
        processed_docs.append(processed_doc)
    
    save_cache(cache)
    return processed_docs

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
        
        # Import the store_in_neo4j function from the correct module
        from store_data_neo4j import store_in_neo4j
        store_in_neo4j(processed_docs)
        
        console.print("[green]✅ Successfully stored data in Neo4j![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        exit(1)
