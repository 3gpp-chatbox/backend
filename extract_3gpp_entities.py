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
import logging

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
            # Network Elements
            "NETWORK_ELEMENT": [
                r'\b(?:UE|AMF|SMF|UDM|AUSF|SEAF|MME|gNB|ng-eNB)\b',
                r'\b(?:Access and Mobility Management Function|Session Management Function)\b',
                r'\b(?:User Equipment|Authentication Server Function|Security Anchor Function)\b',
                r'\b(?:Next Generation Node B|Next Generation eNodeB)\b'
            ],
            
            # NAS Message Categories
            "MM_MESSAGE": [
                r'\b(?:Attach|Detach)\s+(?:Request|Accept|Complete|Reject)\b',
                r'\bTracking\s+Area\s+Update\s+Request\b',
                r'\bService\s+Request\b',
                r'\bIdentity\s+(?:Request|Response)\b'
            ],
            "SM_MESSAGE": [
                r'\bPDU\s+Session\s+(?:Establishment|Release|Modification)\s+(?:Request|Accept|Reject)\b',
                r'\bBearer\s+Resource\s+Modification\s+Request\b'
            ],
            "SECURITY_MESSAGE": [
                r'\bAuthentication\s+(?:Request|Response)\b',
                r'\bSecurity\s+Mode\s+Command\b',
                r'\bIntegrity\s+Protection\s+(?:Activation|Command)\b',
                r'\bCiphering\s+(?:Mode|Activation)\b'
            ],
            
            # State Machines
            "STATE_MACHINE": [
                r'\bRRC-(?:CONNECTED|IDLE)\b',
                r'\b(?:REGISTERED|DEREGISTERED)\b',
                r'\bCM-(?:CONNECTED|IDLE)\b',
                r'\bPDU\s+Session\s+(?:ACTIVE|INACTIVE)\b'
            ],
            
            # Security Mechanisms
            "SECURITY_ALGORITHM": [
                r'\bEAP-AKA\b',
                r'\b5G-AKA\b',
                r'\bSUCI/SUPI\s+protection\b',
                r'\bIntegrity\s+Protection\b',
                r'\bNAS\s+Encryption\b'
            ],
            
            # NAS Timers
            "NAS_TIMER": [
                r'\bT3(?:412|513|550)\b',  # Specific important timers
                r'\bT3[0-9]{3}[a-z]?\b',  # Generic timer pattern
                r'\bT3(?:510|511|512|513|515|516|517|520|522|525|540)\b',  # 5G Timers
                r'\bT3(?:410|411|412|413|415|416|417|420|421|423|440)\b'   # EPS Timers
            ],
            
            # NAS Identifiers
            "NAS_IDENTIFIER": [
                r'\b(?:5G-)?GUTI\b',
                r'\bSUCI\b',
                r'\bSUPI\b',
                r'\bS-TMSI\b',
                r'\b(?:5G-)?S-TMSI\b',
                r'\bIMSI\b',
                r'\bIMEI(?:-SV)?\b',
                r'\bPEI\b'
            ],
            
            # NAS Procedures
            "PROCEDURE": [
                # Main Procedures
                r'\b(?:Initial|Mobility|Periodic|Emergency)\s+Registration\s+Procedure\b',
                r'\b(?:UE|Network)-initiated\s+De-registration\s+Procedure\b',
                r'\b(?:Service\s+Request|PDU\s+Session\s+Establishment)\s+Procedure\b',
                r'\b(?:Handover|Tracking Area Update)\s+Procedure\b',
                # Sub-procedures
                r'\b(?:Authentication|Security Mode Control|Identity)\s+Procedure\b',
                r'\b(?:UE Configuration Update|QoS Flow Establishment)\s+Procedure\b',
                r'\b(?:PDU Session Resource Setup|Service Accept|Service Reject)\s+Procedure\b'
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
                "description": "Establish a PDU session for data connectivity",
                "sub_procedures": [
                    ("QoS Flow Establishment", "6.2.1", "Establish QoS flows for the PDU session"),
                    ("PDU Session Resource Setup", "6.4.1.2", "Setup network resources for PDU session")
                ]
            }
        }

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract all entities from text using compiled patterns"""
        entities = {entity_type: [] for entity_type in self.patterns.keys()}
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    entity = match.group().strip()
                    if entity not in entities[entity_type]:
                        entities[entity_type].append(entity)
        
        return entities

    def extract_procedure_flow(self, text: str, procedure_name: str) -> List[ExecutionStep]:
        """Extract procedure flow steps for a specific procedure"""
        steps = []
        step_number = 1
        
        # Look for numbered steps or sequential indicators
        step_patterns = [
            r'(?:Step|)\s*(\d+)[:.]\s*([^.]+)',  # Numbered steps
            r'(?:First|Then|Next|Finally)[,\s]+([^.]+)'  # Sequential indicators
        ]
        
        for pattern in step_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                step_text = match.group(2) if len(match.groups()) > 1 else match.group(1)
                
                # Extract actor and action
                actor_pattern = r'(?:UE|AMF|SMF|MME|Network)'
                actors = re.findall(actor_pattern, step_text)
                actor = actors[0] if actors else "System"
                
                # Extract parameters
                parameters = []
                for param_pattern in self.patterns['NAS_IDENTIFIER']:
                    params = re.findall(param_pattern, step_text)
                    parameters.extend(params)
                
                # Extract conditions
                conditions = []
                condition_pattern = r'if\s+([^,\.]+)'
                condition_matches = re.finditer(condition_pattern, step_text)
                for cond_match in condition_matches:
                    conditions.append(cond_match.group(1).strip())
                
                step = ExecutionStep(
                    step_number=step_number,
                    actor=actor,
                    action=step_text.strip(),
                    parameters=parameters,
                    conditions=conditions
                )
                
                steps.append(step)
                step_number += 1
        
        return steps

    def extract_state_transitions(self, text: str) -> List[Tuple[str, str, List[str]]]:
        """Extract state transitions and their conditions"""
        transitions = []
        state_pattern = r'(?:EMM|MM|GMM|5GMM)-[A-Z-]+'
        
        # Find all states in the text
        states = re.findall(state_pattern, text)
        
        # Look for transitions between states
        for i, state1 in enumerate(states):
            if i + 1 < len(states):
                state2 = states[i + 1]
                
                # Find conditions between these states
                start_idx = text.find(state1)
                end_idx = text.find(state2)
                if start_idx != -1 and end_idx != -1:
                    between_text = text[start_idx:end_idx]
                    
                    # Extract conditions
                    conditions = []
                    condition_pattern = r'if\s+([^,\.]+)'
                    condition_matches = re.finditer(condition_pattern, between_text)
                    for match in condition_matches:
                        conditions.append(match.group(1).strip())
                    
                    transitions.append((state1, state2, conditions))
        
        return transitions

    def process_document(self, file_path: str) -> Dict:
        """Process a single document and extract all relevant information"""
        try:
            with open(file_path, 'rb') as file:
                pdf = PdfReader(file)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                
                # Extract all entities
                entities = self.extract_entities(text)
                
                # Extract procedure flows for known procedures
                procedure_flows = {}
                for proc_name in self.known_procedures.keys():
                    if proc_name.lower() in text.lower():
                        flow_steps = self.extract_procedure_flow(text, proc_name)
                        procedure_flows[proc_name] = flow_steps
                
                # Extract state transitions
                state_transitions = self.extract_state_transitions(text)
                
                return {
                    "file_path": file_path,
                    "entities": entities,
                    "procedure_flows": procedure_flows,
                    "state_transitions": state_transitions
                }
                
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}")
            return None

def main():
    console.print("[bold blue]Starting 3GPP NAS Entity Extraction[/bold blue]")
    
    # Initialize extractor
    extractor = ThreeGPPEntityExtractor()
    
    # Load cache
    cache = load_cache()
    
    # Process PDF files
    pdf_dir = "data"
    processed_files = []
    
    for file_name in os.listdir(pdf_dir):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(pdf_dir, file_name)
            file_hash = get_file_hash(file_path)
            
            # Check if file was already processed
            if file_hash in cache:
                console.print(f"[yellow]Skipping already processed file: {file_name}[/yellow]")
                processed_files.append(cache[file_hash])
                continue
            
            console.print(f"[green]Processing file: {file_name}[/green]")
            result = extractor.process_document(file_path)
            
            if result:
                cache[file_hash] = result
                processed_files.append(result)
    
    # Save updated cache
    save_cache(cache)
    
    # Store results in Neo4j
    try:
        graph = KnowledgeGraph()
        for file_result in processed_files:
            # Store entities
            for entity_type, entities in file_result["entities"].items():
                for entity in entities:
                    graph.create_entity(entity, entity_type)
            
            # Store procedure flows
            for proc_name, steps in file_result["procedure_flows"].items():
                graph.create_procedure(proc_name, steps)
            
            # Store state transitions
            for from_state, to_state, conditions in file_result["state_transitions"]:
                graph.create_state_transition(from_state, to_state, conditions)
        
        console.print("[bold green]Successfully stored results in Neo4j[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Error storing results in Neo4j: {str(e)}[/bold red]")
    
    console.print("[bold blue]Entity extraction completed[/bold blue]")

if __name__ == "__main__":
    main() 