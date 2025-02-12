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
        # Enhanced regex patterns for different entity types
        self.patterns = {
            "PROCEDURE": [
                r'\b(?:Initial|Service|Periodic|Emergency|Normal)\s+(?:Registration|Attach)\b',
                r'\b(?:UE|Network|NAS|RRC|AMF|SMF)-(?:triggered|initiated)\s+(?:procedure|request)\b',
                r'\b(?:EPS|5GS)\s+(?:Bearer|Session|Mobility)\s+(?:Setup|Release|Modification)\b',
                r'\b(?:Authentication|Security|Identity)\s+(?:Procedure|Request|Response)\b',
                r'\b(?:PDU Session|Bearer|Handover|Tracking Area Update|Paging)\s+(?:Procedure|Request|Response)\b',
                r'\b(?:Attach|Detach|Registration)\s+(?:Procedure|Request|Response)\b',
                r'\b(?:Service|Connection|Resource)\s+(?:Request|Setup|Release)\s+(?:Procedure)\b'
            ],
            "MESSAGE": [
                r'\b(?:NAS|RRC|NGAP|S1AP|N1|N2|N4|N11)\s+(?:Message|PDU|Signal|IE)\b',
                r'\b(?:Authentication|Identity|Security|Configuration|Status)\s+(?:Request|Response|Command|Message|Report)\b',
                r'\b(?:Downlink|Uplink)\s+(?:NAS|RRC|NGAP|Transport)\s+(?:Message|PDU)\b',
                r'\b(?:PDU Session|Bearer|Handover|Registration)\s+(?:Request|Response|Command|Accept|Reject|Complete)\b',
                r'\b(?:Initial|Service|Identity)\s+(?:Request|Response|Accept|Reject)\b',
                r'\b(?:Security Mode|Authentication)\s+(?:Command|Complete|Reject)\b'
            ],
            "NETWORK_ELEMENT": [
                r'\b(?:AMF|SMF|UPF|PCF|UDM|AUSF|NRF|NEF|NSSF|UE|gNB|ng-eNB|MME|SGW|PGW|SGSN|HSS|AF|DN|RAN)\b',
                r'\b(?:Access and Mobility Management Function|Session Management Function|User Plane Function)\b',
                r'\b(?:Policy Control Function|Network Slice Selection Function|Network Exposure Function)\b',
                r'\b(?:Next Generation|5G|Core|Radio Access)\s+(?:Node|Network|Function)\b',
                r'\b(?:Master|Secondary|Target|Source)\s+(?:gNB|ng-eNB|Node B|eNodeB)\b',
                r'\b(?:Access Network|Core Network|Radio Network)\b'
            ],
            "PROTOCOL": [
                r'\b(?:NAS|RRC|NGAP|S1AP|HTTP|MQTT|TCP|UDP|SCTP|GTP|PFCP)\s+(?:Protocol|Signalling|Layer|Stack)\b',
                r'\b(?:5G|LTE|EPS|NR)\s+(?:Protocol|Stack|Architecture)\b',
                r'\b(?:Control Plane|User Plane|Management Plane)\s+(?:Protocol|Stack)\b',
                r'\b(?:N1|N2|N3|N4|N6|N9|N11|N12|N13|N14)\s+(?:Interface|Reference Point)\b',
                r'\b(?:Signalling|Transport|Application)\s+(?:Protocol|Layer)\b'
            ],
            "STATE": [
                r'\b(?:CM-IDLE|CM-CONNECTED|RM-REGISTERED|RM-DEREGISTERED)\b',
                r'\b(?:EMM|ECM|RRC|PMM)-(?:IDLE|CONNECTED|REGISTERED|DEREGISTERED)\b',
                r'\b(?:5GMM|EMM|RRC)\s+(?:State|Mode)\b',
                r'\b(?:Idle|Connected|Active|Inactive)\s+(?:State|Mode)\b'
            ],
            "SPECIFICATION": [
                r'TS\s+\d+\.\d+(?:\.\d+)?',
                r'3GPP\s+(?:TS|TR)\s+\d+\.\d+(?:\.\d+)?',
                r'Release\s+(?:1[0-9]|20)',
                r'Rel-(?:1[0-9]|20)'
            ]
        }
        
        # Compile all patterns
        self.compiled_patterns = {
            entity_type: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for entity_type, patterns in self.patterns.items()
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

    def extract_relationships(self, text: str, entities: Set[Tuple[str, str]]) -> List[Tuple[str, str, str]]:
        """Extract relationships between entities based on proximity and type"""
        relationships = []
        # Split text into sentences more accurately
        sentences = [s.strip() for s in re.split(r'[.!?]+(?=(?:[A-Z]|\s|$))', text) if s.strip()]
        entity_dict = {entity[0].lower(): (entity[0], entity[1]) for entity in entities}
        
        for sentence in sentences:
            sentence = sentence.lower().strip()
            found_entities = []
            
            # Find entities in this sentence
            for entity_text in entity_dict:
                if entity_text in sentence:
                    found_entities.append(entity_dict[entity_text])
            
            # Create relationships between entities in the same sentence
            for i in range(len(found_entities)):
                for j in range(i + 1, len(found_entities)):
                    entity1, type1 = found_entities[i]
                    entity2, type2 = found_entities[j]
                    
                    # Define relationship based on entity types and context
                    relationship = self._determine_relationship(sentence, entity1, type1, entity2, type2)
                    if relationship:
                        relationships.append((entity1, entity2, relationship))
        
        return relationships

    def _determine_relationship(self, sentence: str, entity1: str, type1: str, entity2: str, type2: str) -> str:
        """Determine the relationship type based on entity types and sentence context"""
        # Convert to lower case for matching
        sentence = sentence.lower()
        entity1_lower = entity1.lower()
        entity2_lower = entity2.lower()
        
        # Enhanced relationship patterns
        patterns = {
            'sends': r'(?:sends?|transmits?|forwards?|delivers?)',
            'receives': r'(?:receives?|accepts?|processes?)',
            'contains': r'(?:contains?|includes?|carries?|comprises?)',
            'initiates': r'(?:initiates?|triggers?|starts?|begins?)',
            'connects': r'(?:connects?|links?|binds?|associates?)',
            'uses': r'(?:uses?|utilizes?|employs?|requires?)',
            'manages': r'(?:manages?|controls?|handles?|administers?)',
            'transitions': r'(?:transitions?|changes?|moves?|switches?)',
            'authenticates': r'(?:authenticates?|verifies?|validates?)',
            'registers': r'(?:registers?|attaches?|connects?)',
            'deregisters': r'(?:deregisters?|detaches?|disconnects?)'
        }
        
        # Check entity type combinations for specific relationships
        if type1 == "PROCEDURE" and type2 == "MESSAGE":
            if re.search(f"{entity1_lower}.*{patterns['contains']}.*{entity2_lower}", sentence):
                return "USES_MESSAGE"
            if re.search(f"{entity1_lower}.*{patterns['sends']}.*{entity2_lower}", sentence):
                return "SENDS"
            return "INVOLVES"
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "PROCEDURE":
            if re.search(f"{entity1_lower}.*{patterns['initiates']}.*{entity2_lower}", sentence):
                return "INITIATES"
            if re.search(f"{entity1_lower}.*{patterns['manages']}.*{entity2_lower}", sentence):
                return "MANAGES"
            return "PERFORMS"
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "MESSAGE":
            if re.search(f"{entity1_lower}.*{patterns['sends']}.*{entity2_lower}", sentence):
                return "SENDS"
            if re.search(f"{entity1_lower}.*{patterns['receives']}.*{entity2_lower}", sentence):
                return "RECEIVES"
            return "PROCESSES"
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "STATE":
            if re.search(f"{entity1_lower}.*{patterns['transitions']}.*{entity2_lower}", sentence):
                return "TRANSITIONS_TO"
            return "CAN_BE_IN"
            
        elif type1 == "PROTOCOL" and type2 in ["MESSAGE", "PROCEDURE"]:
            if re.search(f"{entity1_lower}.*{patterns['contains']}.*{entity2_lower}", sentence):
                return "CONTAINS"
            return "DEFINES"
            
        elif type1 == "NETWORK_ELEMENT" and type2 == "NETWORK_ELEMENT":
            if re.search(f"{entity1_lower}.*{patterns['sends']}.*{entity2_lower}", sentence):
                return "SENDS_TO"
            if re.search(f"{entity1_lower}.*{patterns['connects']}.*{entity2_lower}", sentence):
                return "CONNECTS_TO"
            if re.search(f"{entity1_lower}.*{patterns['manages']}.*{entity2_lower}", sentence):
                return "MANAGES"
            return "INTERACTS_WITH"
            
        elif type1 == "PROCEDURE" and type2 == "STATE":
            if re.search(f"{entity1_lower}.*{patterns['transitions']}.*{entity2_lower}", sentence):
                return "RESULTS_IN"
            return "INVOLVES"
            
        elif type1 == "SPECIFICATION" or type2 == "SPECIFICATION":
            if re.search(f"{entity1_lower}.*{patterns['contains']}.*{entity2_lower}", sentence):
                return "DEFINES"
            return "REFERENCED_IN"
        
        return None

def process_documents(documents: List[Dict[str, str]]) -> List[Dict]:
    """Process documents to extract entities and relationships"""
    processed_docs = []
    cache = load_cache()
    extractor = ThreeGPPEntityExtractor()
    
    for doc in documents:
        file_path = doc["metadata"]["file_path"]
        # Calculate hash of the file
        file_hash = get_file_hash(file_path)
        
        # Check if file is in cache and hash matches
        if file_path in cache and cache[file_path]["hash"] == file_hash:
            console.print(f"[green]Using cached results for {file_path}[/green]")
            processed_docs.append(cache[file_path]["data"])
            continue
            
        console.print(f"[blue]Processing {file_path}[/blue]")
        text = doc["text"]
        
        # Extract entities and relationships
        entities = extractor.extract_entities(text)
        relationships = extractor.extract_relationships(text, entities)
        
        # Create processed document
        processed_doc = {
            "entities": list(entities),
            "relationships": list(relationships),
            "metadata": doc["metadata"]
        }
        
        # Update cache
        cache[file_path] = {
            "hash": file_hash,
            "data": processed_doc
        }
        
        processed_docs.append(processed_doc)
    
    # Save updated cache
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
