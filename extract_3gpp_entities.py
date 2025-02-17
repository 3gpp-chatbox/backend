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
from generate_mermaid import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
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
        # Core regex patterns for 3GPP NAS domain with focus on 5G Registration
        self.patterns = {
            # 5G Registration specific patterns
            "REGISTRATION_PROCEDURE": [
                r'(?:Initial|Mobility|Periodic|Emergency)\s+Registration\s+(?:procedure|Procedure)',
                r'Registration\s+(?:Request|Accept|Complete|Reject)',
                r'(?:UE|AMF)-initiated\s+Registration',
                r'5G(?:S|MM)\s+Registration'
            ],
            
            # 5G States
            "5G_STATE": [
                r'5GMM-(?:REGISTERED|DEREGISTERED|IDLE|CONNECTED)',
                r'5GMM-(?:REGISTERED)\.(?:NORMAL-SERVICE|UPDATE-NEEDED|ATTEMPTING-TO-UPDATE|LIMITED-SERVICE)',
                r'5GMM-(?:DEREGISTERED)\.(?:NORMAL-SERVICE|ATTEMPTING-REGISTRATION|LIMITED-SERVICE|NO-CELL-AVAILABLE)',
                r'RM-(?:REGISTERED|DEREGISTERED)'
            ],
            
            # 5G Network Elements
            "5G_NETWORK_ELEMENT": [
                r'(?:AMF|SMF|UDM|AUSF|SEAF|UPF|gNB|ng-eNB)',
                r'Access and Mobility Management Function',
                r'Session Management Function',
                r'Authentication Server Function',
                r'Security Anchor Function'
            ],
            
            # 5G Messages
            "5G_MESSAGE": [
                r'Registration\s+(?:Request|Accept|Complete|Reject)',
                r'Authentication\s+(?:Request|Response|Result|Reject)',
                r'Security Mode\s+(?:Command|Complete|Reject)',
                r'Identity\s+(?:Request|Response)',
                r'Configuration Update\s+Command'
            ],
            
            # 5G Parameters
            "5G_PARAMETER": [
                r'5G-GUTI',
                r'SUCI',
                r'SUPI',
                r'5G-S-TMSI',
                r'PEI',
                r'(?:Allowed|Rejected)\s+NSSAI',
                r'(?:Request|Configured)\s+NSSAI',
                r'TAI',
                r'5GS\s+(?:registration|update)\s+type',
                r'5GMM\s+capability',
                r'UE\s+security\s+capability'
            ],
            
            # 5G Security
            "5G_SECURITY": [
                r'5G-(?:AKA|EAP)',
                r'SUCI/SUPI\s+de-concealment',
                r'5G\s+security\s+context',
                r'5G\s+NAS\s+security',
                r'KAMF',
                r'5G\s+(?:integrity|ciphering)\s+key'
            ],
            
            # 5G Timers
            "5G_TIMER": [
                r'T3(?:510|511|512|513|515|516|517|520|522|525|540)',
                r'Mobile\s+reachable\s+timer',
                r'Implicit\s+de-registration\s+timer'
            ],
            
            # Procedure Flow Steps
            "PROCEDURE_STEP": [
                r'(?:Step|step)\s+(\d+)[:.]\s*([^.!?\n]+)',
                r'(?:^|\n)\s*(\d+)[).]\s*([^.!?\n]+)',
                r'(?:First|Then|Next|Finally)\s*[,.]\s*([^.!?\n]+)',
                r'(?:shall|must|will)\s+(?:then|subsequently|afterwards)\s+([^.!?\n]+)',
                r'(?:consists of|includes|contains)\s+(?:the following|these)\s+steps?:\s*([^.!?\n]+)'
            ]
        }
        
        # Compile all patterns
        self.compiled_patterns = {
            entity_type: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for entity_type, patterns in self.patterns.items()
        }

        # Known 5G Registration procedure steps
        self.registration_steps = {
            "Initial Registration": [
                {
                    "step": 1,
                    "actor": "UE",
                    "action": "sends Registration Request",
                    "parameters": ["SUCI", "5GS registration type", "5GMM capability"],
                    "description": "UE initiates registration by sending Registration Request with identity and capabilities"
                },
                {
                    "step": 2,
                    "actor": "AMF",
                    "action": "initiates Primary Authentication",
                    "parameters": ["5G-AKA", "SUCI", "SUPI"],
                    "description": "AMF starts authentication procedure to verify UE identity"
                },
                {
                    "step": 3,
                    "actor": "AMF",
                    "action": "sends Security Mode Command",
                    "parameters": ["UE security capability", "5G NAS security algorithms"],
                    "description": "AMF activates NAS security with the UE"
                },
                {
                    "step": 4,
                    "actor": "UE",
                    "action": "sends Security Mode Complete",
                    "parameters": ["IMEISV", "NAS-MAC"],
                    "description": "UE confirms security activation and provides equipment identity if requested"
                },
                {
                    "step": 5,
                    "actor": "AMF",
                    "action": "sends Registration Accept",
                    "parameters": ["5G-GUTI", "Registration result", "Allowed NSSAI"],
                    "description": "AMF accepts registration and provides temporary identity and allowed services"
                },
                {
                    "step": 6,
                    "actor": "UE",
                    "action": "sends Registration Complete",
                    "parameters": ["5G-GUTI"],
                    "description": "UE acknowledges registration completion and new temporary identity"
                }
            ]
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
                for proc_name in self.registration_steps.keys():
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
        graph = KnowledgeGraph(
            uri=NEO4J_URI,
            user=NEO4J_USER,
            password=NEO4J_PASSWORD
        )
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
            
            # Store 5G Registration steps
            for proc_name, steps in extractor.registration_steps.items():
                for step in steps:
                    # Create Action node for the step
                    action_props = {
                        "name": f"{step['actor']} {step['action']}",
                        "actor": step['actor'],
                        "description": step['description'],
                        "step_number": step['step']
                    }
                    graph.create_node("Action", action_props)
                    
                    # Create Parameter nodes and relationships
                    for param in step['parameters']:
                        param_props = {
                            "name": param,
                            "type": "5G_PARAMETER"
                        }
                        graph.create_node("Parameter", param_props)
                        graph.create_relationship(
                            "Action", action_props["name"],
                            "USES_PARAMETER",
                            "Parameter", param
                        )
                    
                    # Create relationships between consecutive steps
                    if step['step'] > 1:
                        prev_step = next(s for s in steps if s['step'] == step['step'] - 1)
                        graph.create_relationship(
                            "Action", f"{prev_step['actor']} {prev_step['action']}",
                            "TRIGGERS",
                            "Action", action_props["name"]
                        )
        
        console.print("[bold green]Successfully stored results in Neo4j[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Error storing results in Neo4j: {str(e)}[/bold red]")
    
    console.print("[bold blue]Entity extraction completed[/bold blue]")

if __name__ == "__main__":
    main() 