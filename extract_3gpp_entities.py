import os
import re
import json
from typing import List, Dict, Tuple, Set
from enum import Enum
from dataclasses import dataclass
from pypdf import PdfReader
from neo4j import GraphDatabase
from preprocess_pdfs import read_pdfs_from_directory
from rich.console import Console
from tqdm import tqdm
import hashlib
from dotenv import load_dotenv
from store_data_neo4j import KnowledgeGraph
from utils.pdf_processor import PDFProcessor
from utils.preprocessing import TextPreprocessor
from utils.database import Neo4jConnection, ChromaDBConnection
from utils.refined_extractor import RefinedExtractor
from utils.validator import DataValidator
from utils.query_interface import GraphQueryInterface
import logging
from utils.pdf_handler import PDFHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define enums and data classes for state management
class StateType(Enum):
    EMM = "EMM"
    MM = "MM"
    GMM = "GMM"
    PMM = "PMM"
    CM = "CM"
    RRC = "RRC"
    FIVE_GMM = "5GMM"

@dataclass
class State:
    name: str
    type: StateType
    description: str
    source_section: str
    conditions: List[str] = None

    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []

@dataclass
class Action:
    name: str
    actor: str
    target: str = None
    outcome: str = None
    parameters: List[str] = None
    prerequisites: List[str] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
        if self.prerequisites is None:
            self.prerequisites = []

@dataclass
class ExecutionStep:
    step_number: int
    actor: str
    action: str
    parameters: List[str] = None
    conditions: List[str] = None
    next_steps: List[int] = None
    alternative_steps: Dict[str, int] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
        if self.conditions is None:
            self.conditions = []
        if self.next_steps is None:
            self.next_steps = []
        if self.alternative_steps is None:
            self.alternative_steps = {}

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

class EntityExtractor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.preprocessor = TextPreprocessor()
        self.neo4j = Neo4jConnection()
        self.chroma = ChromaDBConnection()
        self.validator = DataValidator()
        self.query_interface = GraphQueryInterface(self.neo4j)
        self.extractor = RefinedExtractor()

    def process_all_documents(self):
        """Process all PDFs in the data directory"""
        try:
            logger.info("Starting document processing...")
            # Use existing preprocessing functionality
            documents = read_pdfs_from_directory(self.data_dir)
            
            if not documents:
                logger.warning("No documents found or processed")
                return
            
            for doc in documents:
                try:
                    logger.info(f"Processing document: {doc['metadata']['source']}")
                    self.process_document(doc)
                except Exception as e:
                    logger.error(f"Error processing {doc['metadata']['source']}: {str(e)}")
            
            logger.info("Document processing completed")
            
        except Exception as e:
            logger.error(f"Error in process_all_documents: {str(e)}")

    def process_document(self, document: Dict):
        """Process a single preprocessed document"""
        try:
            # Extract text from preprocessed document
            text = document['text']
            doc_source = document['metadata']['source']
            logger.info(f"Starting extraction for {doc_source}")
            
            # Extract different components
            states = self.extractor.extract_states(text)
            actions = self.extractor.extract_actions(text)
            flow = self.extractor.extract_execution_flow(text)
            
            logger.info(f"Extracted from {doc_source}:")
            logger.info(f"- {len(states)} states")
            logger.info(f"- {len(actions)} actions")
            logger.info(f"- {1 if flow else 0} procedure flow")
            
            # Track successful stores
            stored_states = 0
            stored_actions = 0
            stored_flows = 0
            
            # Validate and store states
            for i, state in enumerate(states, 1):
                result = self.validator.validate_state(state)
                if result.is_valid:
                    try:
                        self.store_state_in_neo4j(state)
                        stored_states += 1
                        logger.debug(f"Stored state {i}/{len(states)}: {state.name} ({state.type})")
                    except Exception as e:
                        logger.error(f"Failed to store state {state.name}: {str(e)}")
                else:
                    logger.warning(f"Invalid state in {doc_source}: {state.name} - {result.errors}")
            
            # Validate and store actions
            for i, action in enumerate(actions, 1):
                result = self.validator.validate_action(action)
                if result.is_valid:
                    try:
                        self.store_action_in_neo4j(action)
                        stored_actions += 1
                        logger.debug(f"Stored action {i}/{len(actions)}: {action.name} (Actor: {action.actor})")
                    except Exception as e:
                        logger.error(f"Failed to store action {action.name}: {str(e)}")
                else:
                    logger.warning(f"Invalid action in {doc_source}: {action.name} - {result.errors}")
            
            # Validate and store flow
            if flow:
                flow_result = self.validator.validate_execution_flow(flow)
                if flow_result.is_valid:
                    try:
                        self.store_procedure_flow_in_neo4j(flow)
                        stored_flows += 1
                        logger.info(f"Stored procedure flow with {len(flow.steps) if hasattr(flow, 'steps') else 0} steps")
                    except Exception as e:
                        logger.error(f"Failed to store procedure flow: {str(e)}")
                else:
                    logger.warning(f"Invalid flow in {doc_source}: {flow_result.errors}")
            
            # Log summary for this document
            logger.info(f"Storage summary for {doc_source}:")
            logger.info(f"- States: {stored_states}/{len(states)} stored successfully")
            logger.info(f"- Actions: {stored_actions}/{len(actions)} stored successfully")
            logger.info(f"- Flows: {stored_flows}/1 stored successfully")
                
        except Exception as e:
            logger.error(f"Error processing document content: {str(e)}")
            raise

    def store_state_in_neo4j(self, state: State):
        """Store state information in Neo4j"""
        with self.neo4j.connect().session() as session:
            # Create state node
            session.run("""
                MERGE (s:State {name: $name})
                SET s.type = $type,
                    s.description = $description,
                    s.source_section = $section
            """, name=state.name,
                 type=state.type.value,
                 description=state.description,
                 section=state.source_section)
            
            # Store conditions as relationships
            for condition in state.conditions:
                session.run("""
                    MATCH (s:State {name: $state_name})
                    MERGE (c:Condition {text: $condition})
                    MERGE (s)-[:HAS_CONDITION]->(c)
                """, state_name=state.name, condition=condition)

    def store_action_in_neo4j(self, action: Action):
        """Store action information in Neo4j"""
        with self.neo4j.connect().session() as session:
            # Create action node
            session.run("""
                MERGE (a:Action {name: $name})
                SET a.actor = $actor,
                    a.outcome = $outcome
            """, name=action.name,
                 actor=action.actor,
                 outcome=action.outcome)
            
            # Store target if exists
            if action.target:
                session.run("""
                    MATCH (a:Action {name: $action_name})
                    MERGE (t:Entity {name: $target})
                    MERGE (a)-[:TARGETS]->(t)
                """, action_name=action.name, target=action.target)
            
            # Store parameters and prerequisites
            for param in action.parameters:
                session.run("""
                    MATCH (a:Action {name: $action_name})
                    MERGE (p:Parameter {name: $param})
                    MERGE (a)-[:REQUIRES]->(p)
                """, action_name=action.name, param=param)
            
            for prereq in action.prerequisites:
                session.run("""
                    MATCH (a:Action {name: $action_name})
                    MERGE (p:Prerequisite {text: $prereq})
                    MERGE (a)-[:HAS_PREREQUISITE]->(p)
                """, action_name=action.name, prereq=prereq)

    def store_procedure_flow_in_neo4j(self, steps: List[ExecutionStep]):
        """Store procedure flow information in Neo4j"""
        with self.neo4j.connect().session() as session:
            # Store each step
            for step in steps:
                session.run("""
                    MERGE (s:Step {number: $number})
                    SET s.actor = $actor,
                        s.action = $action
                """, number=step.step_number,
                     actor=step.actor,
                     action=step.action)
                
                # Store parameters
                for param in step.parameters:
                    session.run("""
                        MATCH (s:Step {number: $step_num})
                        MERGE (p:Parameter {name: $param})
                        MERGE (s)-[:USES]->(p)
                    """, step_num=step.step_number, param=param)
                
                # Store conditions
                for condition in step.conditions:
                    session.run("""
                        MATCH (s:Step {number: $step_num})
                        MERGE (c:Condition {text: $condition})
                        MERGE (s)-[:HAS_CONDITION]->(c)
                    """, step_num=step.step_number, condition=condition)
                
                # Store next steps
                for next_step in step.next_steps:
                    session.run("""
                        MATCH (s1:Step {number: $current})
                        MATCH (s2:Step {number: $next})
                        MERGE (s1)-[:NEXT]->(s2)
                    """, current=step.step_number, next=next_step)
                
                # Store alternative steps
                for condition, alt_step in step.alternative_steps.items():
                    session.run("""
                        MATCH (s1:Step {number: $current})
                        MATCH (s2:Step {number: $alt})
                        MERGE (s1)-[:ALTERNATIVE {condition: $condition}]->(s2)
                    """, current=step.step_number,
                         alt=alt_step,
                         condition=condition)

def process_documents(documents: List[Dict[str, str]]) -> List[Dict]:
    """Process documents to extract entities and relationships with properties"""
    extractor = ThreeGPPEntityExtractor()
    processed_docs = []
    
    for doc in documents:
        text = doc['text']
        
        # Extract all entities
        entities = extractor.extract_entities(text)
        
        # Extract state transitions
        transitions = extract_state_transitions(text)
        
        # Extract procedure relationships
        procedures = extractor.extract_procedure_relationships(text)
        
        # Process the document
        processed_doc = {
            'source': doc.get('source', 'Unknown'),
            'entities': [{'text': entity[0], 'type': entity[1]} for entity in entities],
            'procedures': procedures,
            'transitions': transitions,
            'relationships': []
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

def extract_procedure_flow(text: str, procedure_name: str) -> Dict:
    """Extract complete procedure flow including states, messages, and descriptions"""
    flow = {
        'name': procedure_name,
        'initial_state': None,
        'final_state': None,
        'steps': [],
        'state_transitions': [],
        'metadata': {}
    }
    
    # State patterns
    state_patterns = {
        'initial': r'(?:Initial|Starting)\s+(?:UE|Network)\s+state:\s*([^.]+)',
        'final': r'(?:Final|End)\s+(?:UE|Network)\s+state:\s*([^.]+)',
        'transition': r'(?:UE|Network)\s+transitions?\s+from\s+(\w+[-\s]*\w+)\s+to\s+(\w+[-\s]*\w+)'
    }
    
    # Message patterns
    message_patterns = {
        'attach': r'(?:Attach|Registration)\s+(?:Request|Accept|Complete|Reject)(?:\s+message)?\s*(?:description)?:?\s*([^.]+)',
        'auth': r'Authentication\s+(?:Request|Response|Failure)(?:\s+message)?\s*(?:description)?:?\s*([^.]+)',
        'security': r'Security\s+Mode\s+(?:Command|Complete)(?:\s+message)?\s*(?:description)?:?\s*([^.]+)',
        'identity': r'Identity\s+(?:Request|Response)(?:\s+message)?\s*(?:description)?:?\s*([^.]+)',
        'esm': r'ESM\s+(?:Information\s+Request|Information\s+Response)(?:\s+message)?\s*(?:description)?:?\s*([^.]+)'
    }
    
    # Extract initial and final states
    for state_type, pattern in state_patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            if state_type == 'initial':
                flow['initial_state'] = {
                    'state': match.group(1).strip(),
                    'description': get_context(text, match.start(), 100)
                }
            elif state_type == 'final':
                flow['final_state'] = {
                    'state': match.group(1).strip(),
                    'description': get_context(text, match.start(), 100)
                }
            elif state_type == 'transition':
                flow['state_transitions'].append({
                    'from_state': match.group(1).strip(),
                    'to_state': match.group(2).strip(),
                    'description': get_context(text, match.start(), 100)
                })
    
    # Extract procedure steps with messages and descriptions
    step_number = 0
    for msg_type, pattern in message_patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            step_number += 1
            step = {
                'step_number': step_number,
                'message_type': msg_type,
                'message': match.group(0).strip(),
                'description': match.group(1).strip() if match.groups() else '',
                'context': get_context(text, match.start(), 100),
                'parameters': extract_parameters(get_context(text, match.start(), 100)),
                'conditions': extract_conditions(get_context(text, match.start(), 100))
            }
            flow['steps'].append(step)
    
    # Sort steps based on their position in the text
    flow['steps'].sort(key=lambda x: x['step_number'])
    
    # Extract metadata
    flow['metadata'] = extract_metadata(text)
    
    return flow

def extract_parameters(text: str) -> List[Dict]:
    """Extract parameters and their descriptions"""
    parameters = []
    patterns = [
        r'(?:mandatory|optional)\s+parameter\s+([A-Za-z0-9_]+)\s*(?::|is|shall be)\s*([^.]+)',
        r'parameter\s+([A-Za-z0-9_]+)\s+(?:is|shall be|must be)\s+([^.]+)',
        r'IE\s+(?:type|value)\s+([A-Za-z0-9_]+)\s*(?::|is|shall be)\s*([^.]+)'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            param = {
                'name': match.group(1).strip(),
                'description': match.group(2).strip() if len(match.groups()) > 1 else '',
                'mandatory': 'mandatory' in text.lower()
            }
            parameters.append(param)
    
    return parameters

def extract_conditions(text: str) -> List[Dict]:
    """Extract conditions and their descriptions"""
    conditions = []
    patterns = [
        r'(?:if|when|unless)\s+([^,\.]+)',
        r'(?:in case|in the event)\s+(?:that|of|when|if)\s+([^,\.]+)',
        r'(?:depending on|based on)\s+([^,\.]+)'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            condition = {
                'condition': match.group(1).strip(),
                'context': get_context(text, match.start(), 100)
            }
            conditions.append(condition)
    
    return conditions

def extract_metadata(text: str) -> Dict:
    """Extract metadata about the procedure"""
    metadata = {
        'specification': None,
        'section': None,
        'release': None
    }
    
    patterns = {
        'specification': r'(?:3GPP\s+)?TS\s+(\d+\.\d+)',
        'section': r'(?:section|clause)\s+(\d+\.\d+\.\d+(?:\.\d+)?)',
        'release': r'(?:Release|Rel\.|R)\s*(\d+)'
    }
    
    for meta_type, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata[meta_type] = match.group(1).strip()
    
    return metadata

def get_context(text: str, position: int, window: int) -> str:
    """Get surrounding context for a match"""
    start = max(0, position - window)
    end = min(len(text), position + window)
    return text[start:end].strip()

class ProcedureExtractor:
    def __init__(self):
        self.known_procedures = {
            "LTE_ATTACH": {
                "name": "LTE Attach Procedure",
                "key_steps": [
                    "Initial UE State",
                    "Attach Request",
                    "Authentication",
                    "Security Mode",
                    "Attach Accept",
                    "Attach Complete",
                    "Final UE State"
                ]
            },
            "REGISTRATION": {
                "name": "5G Registration Procedure",
                "key_steps": [
                    "Initial UE State",
                    "Registration Request",
                    "Authentication",
                    "Security Mode",
                    "Registration Accept",
                    "Registration Complete",
                    "Final UE State"
                ]
            }
            # Add more procedures as needed
        }
    
    def extract_procedure(self, text: str, procedure_type: str) -> Dict:
        """Extract complete procedure information"""
        if procedure_type not in self.known_procedures:
            return None
        
        procedure = self.known_procedures[procedure_type]
        flow = extract_procedure_flow(text, procedure["name"])
        
        # Validate all key steps are found
        missing_steps = []
        for key_step in procedure["key_steps"]:
            found = False
            for step in flow["steps"]:
                if key_step.lower() in step["message"].lower():
                    found = True
                    break
            if not found:
                missing_steps.append(key_step)
        
        if missing_steps:
            print(f"Warning: Missing key steps in {procedure_type}: {', '.join(missing_steps)}")
        
        return flow

def extract_state_transitions(text: str) -> List[Dict]:
    """Extract state transitions with their triggers and conditions"""
    transitions = []
    
    # Enhanced patterns for state transitions
    patterns = [
        # Direct state transitions
        r'(?:from|in)\s+(?:the\s+)?([A-Z0-9-]+(?:\s+(?:state|STATE))?)(?:\s+to|\s+enters?|\s+transitions?\s+to)\s+(?:the\s+)?([A-Z0-9-]+(?:\s+(?:state|STATE))?)',
        
        # EMM/5GMM specific transitions
        r'(?:UE|AMF|MME)\s+(?:changes?|moves?|transitions?)\s+(?:from\s+)?([A-Z0-9-]+(?:\s+(?:state|STATE))?)\s+to\s+([A-Z0-9-]+(?:\s+(?:state|STATE))?)',
        
        # State changes due to procedures
        r'(?:after|upon|when)\s+(?:successful|completing)\s+(?:the\s+)?([A-Za-z\s]+procedure).*?([A-Z0-9-]+(?:\s+(?:state|STATE))?)\s+(?:to|into)\s+([A-Z0-9-]+(?:\s+(?:state|STATE))?)',
        
        # Implicit transitions
        r'(?:while|when)\s+(?:in|at)\s+([A-Z0-9-]+(?:\s+(?:state|STATE))?)[^.]*?(?:changes?|moves?|transitions?)\s+to\s+([A-Z0-9-]+(?:\s+(?:state|STATE))?)',
        
        # EMM/5GMM state machine transitions
        r'EMM state machine transitions from ([A-Z0-9-]+(?:\s+(?:state|STATE))?)\s+to\s+([A-Z0-9-]+(?:\s+(?:state|STATE))?)',
        r'5GMM state machine transitions from ([A-Z0-9-]+(?:\s+(?:state|STATE))?)\s+to\s+([A-Z0-9-]+(?:\s+(?:state|STATE))?)'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            # Get context around the transition
            start_pos = max(0, match.start() - 100)
            end_pos = min(len(text), match.end() + 100)
            context = text[start_pos:end_pos].strip()
            
            # Extract states based on pattern type
            if len(match.groups()) == 2:
                from_state = match.group(1).strip()
                to_state = match.group(2).strip()
                trigger = None
            else:
                trigger = match.group(1).strip()
                from_state = match.group(2).strip()
                to_state = match.group(3).strip()
            
            # Extract any conditions
            conditions = []
            condition_pattern = r'(?:if|when|only if|provided that)\s+([^,\.]+)'
            condition_matches = re.finditer(condition_pattern, context)
            for cond_match in condition_matches:
                conditions.append(cond_match.group(1).strip())
            
            transition = {
                'from_state': from_state,
                'to_state': to_state,
                'trigger': trigger,
                'conditions': conditions,
                'context': context
            }
            transitions.append(transition)
    
    return transitions

def store_state_transitions(graph: KnowledgeGraph, transitions: List[Dict]):
    """Store state transitions in Neo4j"""
    for transition in transitions:
        # Create state nodes if they don't exist
        graph.create_entity(
            transition['from_state'],
            'STATE',
            {'context': transition['context']}
        )
        graph.create_entity(
            transition['to_state'],
            'STATE',
            {'context': transition['context']}
        )
        
        # Create transition relationship with properties
        properties = {
            'context': transition['context']
        }
        if transition['trigger']:
            properties['trigger'] = transition['trigger']
        if transition['conditions']:
            properties['conditions'] = transition['conditions']
        
        graph.create_relationship(
            transition['from_state'],
            transition['to_state'],
            'TRANSITIONS_TO',
            properties
        )

# Update the main execution
if __name__ == "__main__":
    DATA_DIR = os.getenv("DATA_DIR", "data")
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    
    if not NEO4J_PASSWORD:
        console.print("[red]❌ Error: NEO4J_PASSWORD environment variable must be set[/red]")
        exit(1)
    
    try:
        extractor = EntityExtractor(DATA_DIR)
        console.print("[blue]🔍 Processing 3GPP documents...[/blue]")
        extractor.process_all_documents()
        console.print("[green]✅ Processing complete![/green]")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        exit(1)
