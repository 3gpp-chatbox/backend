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
load_dotenv()  # This will load the variables from the .env file


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
        # Core patterns for Mobility Management analysis
        self.patterns = {
            "UE": [
                # UE Patterns
                r'\b(?:UE|User Equipment)\b',
                r'\b(?:Mobile Station|MS)\b',
                r'\b(?:UE|MS)\s+(?:ID|Identifier|Identity)\b',
                r'\b(?:UE|MS)\s+(?:Status|State|Mode)\b'
            ],
            "AMF": [
                # AMF Patterns
                r'\b(?:AMF|Access and Mobility Management Function)\b',
                r'\b(?:AMF)\s+(?:ID|Identifier|Region|Set)\b',
                r'\b(?:AMF)\s+(?:Status|State|Capacity)\b',
                r'\b(?:AMF)\s+(?:Selection|Reselection)\b'
            ],
            "REGISTRATION": [
                # Registration Patterns
                r'\b(?:Initial|Periodic|Emergency)\s+Registration\b',
                r'\b(?:Registration|Update)\s+(?:Request|Accept|Reject|Complete)\b',
                r'\b(?:Registration)\s+(?:Area|Timer|Status)\b',
                r'\b(?:Registration)\s+(?:Type|Procedure|Flow)\b'
            ],
            "DEREGISTRATION": [
                # Deregistration Patterns
                r'\b(?:UE|Network)-initiated\s+Deregistration\b',
                r'\b(?:Deregistration)\s+(?:Request|Accept|Reject)\b',
                r'\b(?:Deregistration)\s+(?:Type|Procedure|Flow)\b',
                r'\b(?:Implicit|Explicit)\s+Deregistration\b'
            ],
            "CONNECTION": [
                # Connection Patterns
                r'\b(?:RRC|CM|RM)\s+(?:Connected|Idle|Inactive)\b',
                r'\b(?:Connection)\s+(?:Setup|Release|Modify)\b',
                r'\b(?:Connection)\s+(?:State|Status|Type)\b',
                r'\b(?:PDU|Bearer)\s+(?:Session|Connection)\b'
            ],
            "NETWORK_AREA": [
                # Network Area Patterns
                r'\b(?:Tracking|Registration|Location)\s+Area\b',
                r'\b(?:TA|RA|LA)\s+(?:Code|Identity|List)\b',
                r'\b(?:Cell|Sector|Coverage)\s+(?:ID|Area)\b',
                r'\b(?:PLMN|Network)\s+(?:ID|Code|Area)\b'
            ],
            "MOBILITY_EVENT": [
                # Mobility Event Patterns
                r'\b(?:Handover|Cell Reselection|Cell Change)\b',
                r'\b(?:Mobility)\s+(?:Event|Trigger|Update)\b',
                r'\b(?:Location|Area)\s+(?:Update|Change)\b',
                r'\b(?:Inter|Intra)-(?:System|RAT|Cell)\s+(?:Handover|Change)\b'
            ],
            "PROCEDURE_TYPE": [
                # Procedure Type Patterns
                r'\b(?:Initial|Periodic|Emergency)\s+(?:Registration|Update)\b',
                r'\b(?:Service|Tracking Area)\s+(?:Request|Update)\b',
                r'\b(?:Authentication|Security Mode|Identity)\s+(?:Procedure)\b',
                r'\b(?:N1|N2|NAS)\s+(?:Message|Procedure|Flow)\b'
            ]
        }

        # Define relationships between entities
        self.relationships = {
            "UE_TO_AMF": [
                r'(?:UE|MS)\s+(?:registers|connects|attaches)\s+(?:with|to)\s+(?:AMF)',
                r'(?:AMF)\s+(?:serves|manages|handles)\s+(?:UE|MS)',
                r'(?:UE|MS)\s+(?:authentication|security)\s+(?:with|by)\s+(?:AMF)'
            ],
            "UE_TO_AREA": [
                r'(?:UE|MS)\s+(?:moves|enters|leaves)\s+(?:Tracking|Registration|Location)\s+Area',
                r'(?:UE|MS)\s+(?:performs|initiates)\s+(?:cell|area)\s+(?:change|update)',
                r'(?:Mobility|Location)\s+(?:event|update)\s+(?:for|by)\s+(?:UE|MS)'
            ],
            "AMF_TO_AREA": [
                r'(?:AMF)\s+(?:manages|controls|serves)\s+(?:Tracking|Registration|Location)\s+Area',
                r'(?:AMF)\s+(?:handles|processes)\s+(?:area|location)\s+(?:update|change)',
                r'(?:Area|Location)\s+(?:managed|controlled)\s+(?:by)\s+(?:AMF)'
            ],
            "PROCEDURE_FLOW": [
                r'(?:Initial|Periodic|Emergency)\s+(?:Registration)\s+(?:procedure|flow)',
                r'(?:Service|Tracking Area)\s+(?:Request|Update)\s+(?:procedure|flow)',
                r'(?:Deregistration|Authentication)\s+(?:procedure|flow)'
            ]
        }

        # Properties for entities
        self.property_patterns = {
            "UE_PROPERTIES": [
                "ID",
                "Status",
                "Registration_Time",
                "Connection_State",
                "Security_Context",
                "5G_GUTI",
                "Location"
            ],
            "AMF_PROPERTIES": [
                "AMF_ID",
                "AMF_Region",
                "AMF_Set",
                "Capacity",
                "Status",
                "Served_Areas",
                "Load_Level"
            ],
            "REGISTRATION_PROPERTIES": [
                "Type",
                "Status",
                "Timestamp",
                "Result",
                "Cause",
                "Follow_On_Request",
                "Update_Type"
            ],
            "CONNECTION_PROPERTIES": [
                "State",
                "Type",
                "Quality",
                "Establishment_Cause",
                "Release_Cause",
                "Duration",
                "PDU_Sessions"
            ],
            "AREA_PROPERTIES": [
                "Area_Code",
                "PLMN_ID",
                "TAC",
                "Cell_ID",
                "Access_Type",
                "Coverage_Level",
                "Congestion_Level"
            ],
            "EVENT_PROPERTIES": [
                "Event_Type",
                "Trigger",
                "Timestamp",
                "Source_Area",
                "Target_Area",
                "Result",
                "Cause"
            ]
        }

    def extract_entities(self, text: str) -> Set[Tuple[str, str]]:
        """Extract entities using regex patterns"""
        entities = set()
        
        # Apply each pattern and collect entities
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    entity_text = match.group().strip()
                    # Normalize entity text to handle case variations
                    if entity_type in ["NETWORK_ELEMENT", "PROTOCOL", "STATE"]:
                        entity_text = entity_text.upper()
                    else:
                        entity_text = entity_text.title()
                    entities.add((entity_text, entity_type))
        
        return entities
    
    def _normalize_entity_text(self, text: str, entity_type: str) -> str:
        """Normalize entity text based on its type."""
        if entity_type in ["NETWORK_ELEMENT", "PROTOCOL", "STATE"]:
            return text.upper()  # For network-related types, make it uppercase
        return text.title()  # Otherwise, convert to title case

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

        # Check for matching patterns in the sentence
        for relationship, pattern in patterns.items():
            if re.search(pattern, sentence):
                return relationship, properties

        return 'unknown_relationship', properties  # Return a default if no pattern matches

    def extract_relationships(self, text: str, entities: Set[Tuple[str, str]]) -> List[Tuple[str, str, str, Dict]]:
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


    def _match_relationship(self, entity1, entity2, pattern_key, sentence):
        """Helper function to match relationship patterns."""
        entity1_lower = re.escape(entity1.lower())
        entity2_lower = re.escape(entity2.lower())
        pattern = self.patterns.get(pattern_key)

        if not pattern:
            return None, {}  # Return early if the pattern is not found

        # Using re.finditer correctly with re module
        matches = re.finditer(f"{entity1_lower}.*{pattern}.*{entity2_lower}", sentence)

        # Return the first match or None if there are no matches
        for match in matches:
            return match, pattern

        return None, {}

    def map_relationship(self, entity1, type1, entity2, type2, sentence):
        """Main function to map relationships."""
        if type1 == "PROCEDURE" and type2 == "MESSAGE":
            match, pattern = self._match_relationship(entity1, entity2, 'uses', sentence)
            if match:
                return "USES_MESSAGE", {"pattern": pattern}

        elif type1 == "NETWORK_ELEMENT" and type2 == "PROCEDURE":
            match, pattern = self._match_relationship(entity1, entity2, 'initiates', sentence)
            if match:
                return "INITIATES", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'performs', sentence)
            if match:
                return "PERFORMS", {"pattern": pattern}

        elif type1 == "NETWORK_ELEMENT" and type2 == "MESSAGE":
            match, pattern = self._match_relationship(entity1, entity2, 'sends', sentence)
            if match:
                return "SENDS", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'receives', sentence)
            if match:
                return "RECEIVES", {"pattern": pattern}

        elif type1 == "NETWORK_ELEMENT" and type2 == "NETWORK_ELEMENT":
            match, pattern = self._match_relationship(entity1, entity2, 'communicates', sentence)
            if match:
                return "COMMUNICATES_WITH", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'authenticates', sentence)
            if match:
                return "AUTHENTICATES", {"pattern": pattern}

        elif type1 == "PROTOCOL" and type2 in ["MESSAGE", "PROCEDURE"]:
            match, pattern = self._match_relationship(entity1, entity2, 'defines', sentence)
            if match:
                return "DEFINES", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'uses', sentence)
            if match:
                return "USES", {"pattern": pattern}

        elif type1 == "STATE" and type2 == "PROCEDURE":
            match, pattern = self._match_relationship(entity2, entity1, 'results', sentence)
            if match:
                return "RESULTS_IN", {"pattern": pattern}

        elif type1 == "SPECIFICATION" and type2 in ["PROCEDURE", "MESSAGE"]:
            match, pattern = self._match_relationship(entity1, entity2, 'defines', sentence)
            if match:
                return "DEFINES", {"pattern": pattern}

        elif type1 == "STATE" and type2 == "STATE":
            match, pattern = self._match_relationship(entity1, entity2, 'transitions', sentence)
            if match:
                return "TRANSITIONS_TO", {"pattern": pattern}

        elif type1 == "ACTION" and type2 == "EVENT":
            match, pattern = self._match_relationship(entity1, entity2, 'triggers', sentence)
            if match:
                return "TRIGGERS", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'handles', sentence)
            if match:
                return "HANDLES", {"pattern": pattern}

        elif type1 == "EVENT" and type2 == "ACTION":
            match, pattern = self._match_relationship(entity1, entity2, 'triggers', sentence)
            if match:
                return "TRIGGERS", {"pattern": pattern}

        elif type1 == "ACTION" and type2 == "STATE":
            match, pattern = self._match_relationship(entity1, entity2, 'results', sentence)
            if match:
                return "RESULTS_IN", {"pattern": pattern}

        elif type1 == "EVENT" and type2 == "PROCEDURE":
            match, pattern = self._match_relationship(entity1, entity2, 'triggers', sentence)
            if match:
                return "TRIGGERS", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'interrupts', sentence)
            if match:
                return "INTERRUPTS", {"pattern": pattern}

        elif type1 == "ACTION" and type2 == "MESSAGE":
            match, pattern = self._match_relationship(entity1, entity2, 'sends', sentence)
            if match:
                return "SENDS", {"pattern": pattern}
            match, pattern = self._match_relationship(entity1, entity2, 'processes', sentence)
            if match:
                return "PROCESSES", {"pattern": pattern}

        return None, {}



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

def extract_entities_and_relationships(documents):
    """Extract entities and relationships from the documents using regex patterns."""
    extracted_entities = []
    extracted_relationships = []

    # Define regex patterns for entities and relationships
    entity_patterns = {
        "UE": r'\b(?:User Equipment|UE)\b',
        "AMF": r'\b(?:Access and Mobility Management Function|AMF)\b',
        "Registration": r'\b(?:Registration)\b',
        "Deregistration": r'\b(?:Deregistration)\b',
        "Connection": r'\b(?:Connection)\b',
        "Network Area": r'\b(?:Network Area)\b',
        "Mobility Event": r'\b(?:Mobility Event)\b',
        "Procedure Type": r'\b(?:Procedure Type)\b',
    }

    relationship_patterns = {
        "REGISTERS_WITH": r'\b(?:UE|User Equipment)\s+(?:registers|attaches)\s+(?:with|to)\s+(?:AMF)\b',
        "DEREGISTERS_FROM": r'\b(?:UE|User Equipment)\s+(?:deregisters|detaches)\s+(?:from)\s+(?:AMF)\b',
        "MOVES_TO": r'\b(?:UE|User Equipment)\s+(?:moves|enters|leaves)\s+(?:Network Area)\b',
        "HANDLES": r'\b(?:AMF)\s+(?:handles|manages)\s+(?:Mobility Event)\b',
    }

    for doc in documents:
        text = doc["text"]

        # Extract entities
        for entity_type, pattern in entity_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                extracted_entities.append({
                    "name": match,
                    "type": entity_type,
                    "properties": {}  # Add any relevant properties if needed
                })

        # Extract relationships
        for rel_type, pattern in relationship_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                # Assuming the relationship involves UE and AMF
                extracted_relationships.append({
                    "from": "User Equipment",  # Adjust based on actual extraction
                    "to": "Access and Mobility Management Function",  # Adjust based on actual extraction
                    "type": rel_type
                })

    return extracted_entities, extracted_relationships
