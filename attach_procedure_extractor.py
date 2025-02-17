import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from preprocess_pdfs import (
    read_pdfs_from_directory, 
    chunk_text,  # Use simple chunking instead of semantic
    is_title_page_content,
    is_toc_content,
    is_index_or_appendix_content
)
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import logging
from rich.console import Console
from rich.logging import RichHandler
import numpy as np
from datetime import datetime
from multiprocessing import Pool, cpu_count
from functools import partial
import hashlib
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
import pdfplumber
import nltk
from sentence_transformers import SentenceTransformer

# Configure rich logging
console = Console()
logging.basicConfig(
    level=logging.ERROR,  # Change to ERROR to show only errors
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True, show_time=False)]  # Disable timestamp
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Neo4j Configuration with debug logging
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

console.print(f"[yellow]Debug: NEO4J_URI={NEO4J_URI}[/yellow]")
console.print(f"[yellow]Debug: NEO4J_USERNAME={NEO4J_USER}[/yellow]")
console.print("[yellow]Debug: NEO4J_PASSWORD=***********[/yellow]")

if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD]):
    console.print("[red]Error: Missing Neo4j credentials in .env file[/red]")
    exit(1)

class StateType(Enum):
    EMM = "EMM"
    MM = "MM"
    GMM = "GMM"
    PMM = "PMM"
    CM = "CM"
    RRC = "RRC"
    FIVE_GMM = "5GMM"

@dataclass(frozen=True)
class State:
    name: str
    type: StateType
    description: str
    conditions: tuple[str, ...] = ()  # Use tuple instead of list
    source_spec: str = None
    section: str = None

    def __hash__(self):
        return hash((self.name, self.type, self.source_spec, self.section))

@dataclass(frozen=True)
class Action:
    name: str
    actor: str
    description: str
    parameters: tuple[str, ...] = ()  # Use tuple instead of list
    prerequisites: tuple[str, ...] = ()  # Use tuple instead of list
    source_spec: str = None
    section: str = None

    def __hash__(self):
        return hash((self.name, self.actor, self.source_spec, self.section))

@dataclass(frozen=True)
class Event:
    name: str
    trigger: str
    description: str
    conditions: tuple[str, ...] = ()  # Use tuple instead of list
    source_spec: str = None
    section: str = None

    def __hash__(self):
        return hash((self.name, self.trigger, self.source_spec, self.section))

@dataclass(frozen=True)
class Parameter:
    name: str
    type: str
    description: str
    mandatory: bool = False
    value_range: str = None
    source_spec: str = None
    section: str = None

    def __hash__(self):
        return hash((self.name, self.type, self.source_spec, self.section))

# Download required NLTK resources
console = Console()
console.print("Checking NLTK resource: stopwords")
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    console.print("Downloading NLTK resource: stopwords")
    nltk.download('stopwords')

console.print("Checking NLTK resource: wordnet")
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    console.print("Downloading NLTK resource: wordnet")
    nltk.download('wordnet')

console.print("Checking NLTK resource: omw-1.4")
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    console.print("Downloading NLTK resource: omw-1.4")
    nltk.download('omw-1.4')

class ThreeGPPExtractor:
    def __init__(self):
        # Core patterns for protocol analysis
        self.patterns = {
            'SECTION': [
                # Section numbers and titles
                r'^\d+(?:\.\d+)*\s+[A-Z]',  # Numbered sections
                r'^Annex [A-Z]',  # Annexes
                r'^(?:Table|Figure)\s+\d+(?:\.\d+)*',  # Tables and Figures
                r'^[A-Z][A-Za-z\s]+$'  # All caps or Title Case headings
            ],
            'STATE': [
                # UE States
                r'(?:EMM|MM|GMM|PMM|CM|RRC|5GMM)-(?:DEREGISTERED|REGISTERED|IDLE|CONNECTED|NULL)',
                r'(?:EMM|MM|GMM|5GMM)-(?:REGISTERED|DEREGISTERED)\.(?:NORMAL-SERVICE|ATTEMPTING-TO-ATTACH|LIMITED-SERVICE|NO-CELL-AVAILABLE)',
                r'(?:EMM|MM|GMM|5GMM)-(?:REGISTERED)\.(?:NORMAL-SERVICE|UPDATE-NEEDED|ATTEMPTING-TO-UPDATE|LIMITED-SERVICE)',
                r'(?:CONNECTED|IDLE|SUSPENDED)\s+(?:state|mode)',
                # Network Element States
                r'(?:MME|AMF|SGSN)-(?:CONNECTED|IDLE|ACTIVE|STANDBY)',
                r'(?:eNB|gNB|RAN)-(?:ACTIVE|INACTIVE|CONNECTED|IDLE)',
                # Bearer States
                r'(?:EPS|PDU|Bearer)-(?:ACTIVE|INACTIVE|SUSPENDED|MODIFIED)'
            ],
            
            'ACTION': [
                # UE Actions
                r'(?:UE|MS)\s+(?:sends?|initiates?|performs?|executes?)\s+(?:Attach|Registration|Service\s+Request|PDU\s+Session)',
                r'(?:UE|MS)\s+(?:starts?|triggers?|requests?)\s+(?:Authentication|Security\s+Mode|Identity)',
                # Network Actions
                r'(?:MME|AMF|SGSN)\s+(?:sends?|allocates?|initiates?)\s+(?:Accept|Reject|Identity\s+Request)',
                r'(?:MME|AMF|SGSN)\s+(?:performs?|executes?)\s+(?:Authentication|Security|Bearer\s+Setup)',
                # Combined Actions
                r'(?:Authentication|Security Mode|Identity|Bearer)\s+(?:procedure|request|response|setup)',
                r'(?:Integrity|Ciphering|NAS-MAC)\s+(?:verification|generation|computation)'
            ],
            
            'EVENT': [
                # Message Reception Events
                r'(?:upon|when|after)\s+receiving\s+(?:Request|Accept|Complete|Reject)',
                r'(?:on|upon)\s+(?:successful|unsuccessful)\s+(?:Authentication|Security|Registration)',
                # Timer Events
                r'(?:T3410|T3411|T3421|T3440|T3450)\s+(?:expires|starts?|stops?)',
                # State Change Events
                r'(?:enters?|transitions?\s+to)\s+(?:EMM|MM|GMM|5GMM)-\w+\s+state',
                # Security Events
                r'(?:Authentication|Security)\s+(?:Success|Failure|Completion|Timeout)',
                # Bearer Events
                r'(?:Bearer|PDU\s+Session)\s+(?:Establishment|Modification|Release)'
            ],
            
            'PARAMETER': [
                # Identity Parameters
                r'(?:IMSI|GUTI|TMSI|SUCI|5G-GUTI)',
                # Bearer Parameters
                r'(?:EPS|PDU|QoS)\s+(?:Bearer|Flow|Parameters)',
                # Security Parameters
                r'(?:Authentication|Security)\s+(?:Vector|Parameter|Key)',
                r'(?:KSI|eKSI|NAS-MAC|RAND|RES|AUTN)',
                # Capability Parameters
                r'(?:UE|Network)\s+(?:Capability|Feature|Support)',
                # Network Parameters
                r'(?:TAI|PLMN|TAC|Cell-ID|ECGI|NR-CGI)',
                # Message Parameters
                r'(?:NAS|RRC|S1AP|NGAP)\s+(?:Message|IE|Container)',
                # QoS Parameters
                r'(?:QCI|ARP|MBR|GBR|AMBR)'
            ],
            
            'FLOW': [
                # Procedure Steps
                r'Step\s+\d+[:.]\s*(?:The\s+)?(?:UE|MME|AMF)\s+(?:sends?|performs?)',
                r'(?:First|Then|Next|Finally)\s+(?:the\s+)?(?:UE|MME|AMF)\s+(?:shall|must|may)',
                # Sequential Indicators
                r'(?:After|Before|Following|Prior\s+to)\s+(?:the|this)\s+(?:step|procedure|message)',
                # Conditional Flow
                r'(?:If|When|In\s+case)\s+(?:the|this)\s+(?:condition|check|verification)\s+(?:succeeds|fails)',
                # Alternative Flow
                r'(?:Otherwise|Alternatively|In\s+case\s+of\s+failure)'
            ],
            
            'CONDITIONAL': [
                # Authentication Conditions
                r'if\s+(?:Authentication|Security Mode)\s+(?:successful|failed|timeout)',
                # Identity Conditions
                r'(?:when|if)\s+(?:IMSI|GUTI|SUCI)\s+is\s+(?:valid|invalid|available)',
                # State Conditions
                r'if\s+(?:UE|MME|AMF)\s+is\s+in\s+(?:EMM|MM|GMM|5GMM)-\w+\s+state',
                # Bearer Conditions
                r'if\s+(?:Bearer|PDU\s+Session)\s+(?:exists|established|released)',
                # Security Conditions
                r'provided\s+that\s+(?:security|authentication|integrity)\s+is\s+(?:complete|verified)',
                # Capability Conditions
                r'if\s+(?:UE|Network)\s+supports?\s+(?:feature|capability|service)'
            ],
            
            'METADATA': [
                # Message Types
                r'Message\s+Type:\s*(?:0x[0-9A-F]{2}|[0-9]+)',
                # Protocol Discriminator
                r'Protocol\s+(?:Discriminator|Identifier):\s*(?:0x[0-9A-F]{2}|[0-9]+)',
                # Timestamps
                r'T(?:3410|3411|3421|3440|3450)\s*=\s*\d+\s*(?:sec|seconds)',
                # Message IDs
                r'Message\s+ID:\s*(?:0x[0-9A-F]{4}|[0-9]+)',
                # Sequence Numbers
                r'Sequence\s+Number:\s*\d+',
                # Cause Values
                r'Cause:\s*(?:0x[0-9A-F]{2}|[0-9]+)',
                # Protocol Version
                r'Version:\s*(?:\d+\.?\d*)',
                # Transaction ID
                r'Transaction\s+ID:\s*(?:0x[0-9A-F]{2}|[0-9]+)'
            ]
        }
        
        # Add debug logging
        console.print("[blue]Initializing ThreeGPPExtractor...[/blue]")
        
        try:
            # Compile regex patterns once during initialization
            self.compiled_patterns = {
                category: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
                for category, patterns in self.patterns.items()
            }
            console.print("[green]Successfully compiled regex patterns[/green]")
        except Exception as e:
            console.print(f"[red]Error compiling patterns: {str(e)}[/red]")
            raise

        # Initialize sentence transformer with error handling
        try:
            console.print("[yellow]Loading sentence transformer model...[/yellow]")
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            console.print("[green]Successfully loaded sentence transformer model: all-MiniLM-L6-v2[/green]")
        except Exception as e:
            console.print(f"[red]Error initializing sentence transformer: {str(e)}[/red]")
            self.sentence_transformer = None
        
        # Cache for semantic similarity calculations
        self.similarity_cache = {}

        # Update Attach-specific patterns to match requirements
        self.attach_patterns = {
            'states': [
                # Initial and Final States
                r'(?:UE|MS)\s+(?:in|enters?|transitions?\s+to)\s+EMM-DEREGISTERED(?:\.[\w-]+)?',
                r'(?:UE|MS)\s+(?:in|enters?|transitions?\s+to)\s+EMM-REGISTERED(?:\.[\w-]+)?',
                # Network States
                r'MME\s+(?:in|enters?|transitions?\s+to)\s+(?:CONNECTED|IDLE)',
                # Intermediate States
                r'(?:AUTHENTICATION|SECURITY MODE|ATTACH)\s+(?:INITIATED|IN_PROGRESS|COMPLETED)',
                # Service States
                r'(?:NORMAL|LIMITED|NO)\s+SERVICE'
            ],
            'actions': [
                # UE Actions
                r'(?:UE|MS)\s+(?:sends?|initiates?|transmits?)\s+ATTACH\s+REQUEST',
                r'(?:UE|MS)\s+(?:sends?|responds?\s+with)\s+ATTACH\s+COMPLETE',
                r'(?:UE|MS)\s+(?:performs?|executes?)\s+security\s+mode\s+procedure',
                # MME Actions
                r'MME\s+(?:initiates?|starts?)\s+authentication(?:\s+procedure)?',
                r'MME\s+(?:sends?|transmits?)\s+SECURITY\s+MODE\s+COMMAND',
                r'MME\s+(?:sends?|transmits?)\s+ATTACH\s+ACCEPT',
                # Authentication Actions
                r'(?:generate|verify)\s+(?:AUTH|AUTN|RAND|RES|XRES)',
                r'(?:derive|compute)\s+(?:K_ASME|NAS\s+keys)'
            ],
            'events': [
                # Message Events
                r'ATTACH\s+REQUEST\s+(?:received|sent)',
                r'AUTHENTICATION\s+(?:REQUEST|RESPONSE|FAILURE)\s+(?:received|sent)',
                r'SECURITY\s+MODE\s+(?:COMMAND|COMPLETE|REJECT)\s+(?:received|sent)',
                r'ATTACH\s+(?:ACCEPT|COMPLETE|REJECT)\s+(?:received|sent)',
                # Timer Events
                r'T3410\s+(?:starts?|expires?|stops?)',  # Attach attempt timer
                r'T3411\s+(?:starts?|expires?|stops?)',  # Attach retry timer
                r'T3450\s+(?:starts?|expires?|stops?)',  # Attach accept timer
                # State Change Events
                r'(?:enters?|transitions?\s+to)\s+EMM-(?:REGISTERED|DEREGISTERED)',
                # Service Events
                r'(?:gains?|loses?)\s+(?:network|service)\s+access'
            ],
            'parameters': [
                # Identity Parameters
                r'(?:IMSI|GUTI|TMSI|OLD\s+GUTI)',
                r'(?:TAI|LAI|RAI|PLMN)',
                # Security Parameters
                r'(?:KSI|eKSI|KASME)',
                r'(?:AUTH|AUTN|RAND|RES|XRES)',
                r'(?:NAS-MAC|NAS\s+COUNT)',
                # Capability Parameters
                r'UE\s+(?:network|security)\s+capabilities',
                r'MS\s+(?:network|security)\s+capabilities',
                r'(?:EPS|E-UTRAN)\s+capabilities',
                # Bearer Parameters
                r'(?:EPS|DEFAULT)\s+bearer\s+context',
                r'QoS\s+parameters',
                # ESM Parameters
                r'ESM\s+message\s+container',
                r'PDN\s+(?:type|address)',
                # Additional Parameters
                r'(?:DRX|TAU)\s+parameters'
            ],
            'conditionals': [
                # Authentication Conditions
                r'if\s+authentication\s+(?:successful|failed)',
                r'when\s+security\s+mode\s+(?:completed|rejected)',
                # Identity Conditions
                r'if\s+(?:IMSI|GUTI|TMSI)\s+is\s+(?:valid|invalid|available)',
                # State Conditions
                r'if\s+UE\s+(?:is|was)\s+in\s+EMM-(?:REGISTERED|DEREGISTERED)',
                # Service Conditions
                r'if\s+(?:normal|limited)\s+service\s+is\s+available',
                # Bearer Conditions
                r'when\s+default\s+bearer\s+is\s+(?:established|activated)',
                # Timer Conditions
                r'if\s+T34[0-9]+\s+(?:expires|running)'
            ],
            'metadata': [
                # Message Types
                r'Message\s+Type:\s*(?:0x[0-9A-F]{2}|[0-9]+)',
                # Protocol Info
                r'Protocol\s+(?:Discriminator|Identifier):\s*(?:0x[0-9A-F]{2}|[0-9]+)',
                # Timestamps
                r'T34[0-9]+\s*=\s*\d+\s*(?:sec|seconds)',
                # Message IDs
                r'Message\s+ID:\s*(?:0x[0-9A-F]{4}|[0-9]+)',
                # Sequence Numbers
                r'Sequence\s+Number:\s*\d+',
                # Cause Values
                r'EMM\s+cause:\s*(?:0x[0-9A-F]{2}|[0-9]+)',
                # Security Context
                r'(?:NAS|EPS)\s+security\s+context:\s*\d+'
            ]
        }

    def calculate_similarity_cached(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity with caching"""
        cache_key = hashlib.md5((text1 + text2).encode()).hexdigest()
        
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]
            
        if self.sentence_transformer:
            try:
                emb1 = self.sentence_transformer.encode(text1, show_progress_bar=False)
                emb2 = self.sentence_transformer.encode(text2, show_progress_bar=False)
                similarity = float(np.dot(emb1, emb2))
                self.similarity_cache[cache_key] = similarity
                return similarity
            except:
                return 0.5
        return 0.5

    def extract_section_context(self, text: str) -> Dict[str, str]:
        """Extract section number and title from text"""
        for line in text.split('\n'):
            for pattern in self.patterns['SECTION']:
                if re.match(pattern, line):
                    return {
                        'section': line.strip(),
                        'context': text[:1000]  # Keep some context
                    }
        return None

    def extract_states(self, text: str, spec_info: Dict) -> List[State]:
        """Extract states specific to Attach procedure"""
        states = []
        for pattern in self.patterns['STATE']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                state_text = match.group().strip()
                
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Determine state type (focus on EMM states for Attach)
                state_type = None
                if 'EMM' in state_text:
                    state_type = StateType.EMM
                elif 'CM' in state_text:
                    state_type = StateType.CM
                
                if state_type:
                    state = State(
                        name=state_text,
                        type=state_type,
                        description=context,
                        conditions=self.extract_conditions(context),
                        source_spec=spec_info.get('source'),
                        section=spec_info.get('section')
                    )
                    
                    # Check for duplicates using semantic similarity
                    if self.sentence_transformer and states:
                        new_embedding = self.sentence_transformer.encode(
                            state.description,
                            show_progress_bar=False
                        )
                        
                        is_duplicate = False
                        for existing_state in states:
                            existing_embedding = self.sentence_transformer.encode(
                                existing_state.description,
                                show_progress_bar=False
                            )
                            similarity = np.dot(new_embedding, existing_embedding)
                            if similarity > 0.85:
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            states.append(state)
                    else:
                        states.append(state)
        
        return states

    def extract_actions(self, text: str, spec_info: Dict) -> List[Action]:
        """Extract actions specific to Attach procedure"""
        actions = []
        for pattern in self.patterns['ACTION']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                action_text = match.group().strip()
                
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Extract actor (UE or MME for Attach procedure)
                actor = None
                if 'UE' in action_text:
                    actor = 'UE'
                elif 'MME' in action_text:
                    actor = 'MME'
                
                if actor:
                    # Extract parameters and convert to strings immediately
                    parameters = self.extract_parameters(context)
                    parameter_names = [p.name if isinstance(p, Parameter) else str(p) for p in parameters]
                    
                    action = Action(
                        name=action_text.replace(actor, '').strip(),
                        actor=actor,
                        description=context,
                        parameters=parameter_names,  # Store as strings
                        prerequisites=self.extract_conditions(context),
                        source_spec=spec_info.get('source'),
                        section=spec_info.get('section')
                    )
                    
                    # Check for duplicates
                    if self.sentence_transformer and actions:
                        new_embedding = self.sentence_transformer.encode(
                            action.description,
                            show_progress_bar=False
                        )
                        
                        is_duplicate = False
                        for existing_action in actions:
                            existing_embedding = self.sentence_transformer.encode(
                                existing_action.description,
                                show_progress_bar=False
                            )
                            similarity = np.dot(new_embedding, existing_embedding)
                            if similarity > 0.85:
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            actions.append(action)
                    else:
                        actions.append(action)
        
        return actions

    def extract_events(self, text: str, spec_info: Dict) -> List[Event]:
        """Extract events specific to Attach procedure"""
        events = []
        for pattern in self.patterns['EVENT']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                event_text = match.group().strip()
                trigger = match.group(1) if match.groups() else event_text
                
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                event = Event(
                    name=event_text,
                    trigger=trigger,
                    description=context,
                    conditions=self.extract_conditions(context),
                    source_spec=spec_info.get('source'),
                    section=spec_info.get('section')
                )
                
                # Check for duplicates
                if self.sentence_transformer and events:
                    new_embedding = self.sentence_transformer.encode(
                        event.description,
                        show_progress_bar=False
                    )
                    
                    is_duplicate = False
                    for existing_event in events:
                        existing_embedding = self.sentence_transformer.encode(
                            existing_event.description,
                            show_progress_bar=False
                        )
                        similarity = np.dot(new_embedding, existing_embedding)
                        if similarity > 0.85:
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        events.append(event)
                else:
                    events.append(event)
        
        return events

    def extract_parameters(self, text: str, spec_info: Dict = None) -> List[Parameter]:
        """Extract parameters specific to Attach procedure"""
        parameters = []
        for pattern in self.patterns['PARAMETER']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                param_text = match.group().strip()
                
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Determine parameter type for Attach procedure
                param_type = 'Unknown'
                if any(id_type in param_text.lower() for id_type in ['imsi', 'guti', 'tmsi']):
                    param_type = 'Identity'
                elif 'security' in param_text.lower():
                    param_type = 'Security'
                elif 'capability' in param_text.lower():
                    param_type = 'Capability'
                elif any(bearer_type in param_text.lower() for bearer_type in ['eps', 'bearer']):
                    param_type = 'Bearer'
                
                # Check if parameter is mandatory
                mandatory = 'mandatory' in context.lower() or 'shall' in context.lower()
                
                parameter = Parameter(
                    name=param_text,
                    type=param_type,
                    description=context,
                    mandatory=mandatory,
                    source_spec=spec_info.get('source') if spec_info else None,
                    section=spec_info.get('section') if spec_info else None
                )
                
                # Check for duplicates
                if self.sentence_transformer and parameters:
                    new_embedding = self.sentence_transformer.encode(
                        parameter.description,
                        show_progress_bar=False
                    )
                    
                    is_duplicate = False
                    for existing_param in parameters:
                        existing_embedding = self.sentence_transformer.encode(
                            existing_param.description,
                            show_progress_bar=False
                        )
                        similarity = np.dot(new_embedding, existing_embedding)
                        if similarity > 0.85:
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        parameters.append(parameter)
                else:
                    parameters.append(parameter)
        
        return parameters

    def extract_conditions(self, text: str) -> List[str]:
        """Extract conditions specific to Attach procedure"""
        conditions = []
        for pattern in self.patterns['CONDITIONAL']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.groups():
                    condition = match.group(1).strip()
                    if condition not in conditions:
                        conditions.append(condition)
        
        return conditions

    def extract_all(self, text: str, spec_info: Dict) -> Dict:
        """Optimized extraction with minimal processing"""
        # Skip irrelevant sections immediately
        if is_title_page_content(text) or is_toc_content(text) or is_index_or_appendix_content(text):
            return None
        
        # Early content check - only process relevant sections
        relevant_keywords = ['attach', 'registration', 'state', 'procedure', '5gmm', 'emm']
        if not any(keyword in text.lower() for keyword in relevant_keywords):
            return None
        
        # Extract section context if available
        section_context = self.extract_section_context(text)
        if section_context:
            spec_info['section'] = section_context['section']
        
        # Process all patterns in a single pass
        entities = {
            'states': set(),  # Using sets to automatically handle duplicates
            'actions': set(),
            'events': set(),
            'parameters': set()
        }
        
        # Single pass extraction with minimal context
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    entity_text = match.group().strip()
                    context_start = max(0, match.start() - 30)  # Reduced context window
                    context_end = min(len(text), match.end() + 30)
                    context = text[context_start:context_end].strip()
                    
                    if category == 'STATE':
                        state_type = None
                        if 'EMM' in entity_text:
                            state_type = StateType.EMM
                        elif 'CM' in entity_text:
                            state_type = StateType.CM
                        
                        if state_type:
                            state = State(
                                name=entity_text,
                                type=state_type,
                                description=context[:500],  # Limit description length
                                source_spec=spec_info.get('source'),
                                section=spec_info.get('section')
                            )
                            entities['states'].add(state)
                    
                    elif category == 'ACTION':
                        actor = None
                        if 'UE' in entity_text:
                            actor = 'UE'
                        elif 'MME' in entity_text:
                            actor = 'MME'
                        
                        if actor:
                            action = Action(
                                name=entity_text.replace(actor, '').strip(),
                                actor=actor,
                                description=context[:500],
                                source_spec=spec_info.get('source'),
                                section=spec_info.get('section')
                            )
                            entities['actions'].add(action)
                    
                    elif category == 'EVENT':
                        event = Event(
                            name=entity_text,
                            trigger=entity_text,
                            description=context[:500],
                            source_spec=spec_info.get('source'),
                            section=spec_info.get('section')
                        )
                        entities['events'].add(event)
                    
                    elif category == 'PARAMETER':
                        param_type = 'Unknown'
                        if any(id_type in entity_text.lower() for id_type in ['imsi', 'guti', 'tmsi']):
                            param_type = 'Identity'
                        elif 'security' in entity_text.lower():
                            param_type = 'Security'
                        
                        parameter = Parameter(
                            name=entity_text,
                            type=param_type,
                            description=context[:500],
                            source_spec=spec_info.get('source'),
                            section=spec_info.get('section')
                        )
                        entities['parameters'].add(parameter)
        
        # Convert sets back to lists for return
        return {
            'states': list(entities['states']),
            'actions': list(entities['actions']),
            'events': list(entities['events']),
            'parameters': list(entities['parameters'])
        }

    def extract_flow(self, text: str, spec_info: Dict) -> List[Dict]:
        """Extract procedure flow steps"""
        flow_steps = []
        step_number = 1
        
        for pattern in self.patterns['FLOW']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                flow_text = match.group().strip()
                
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Extract actors and actions
                actors = re.findall(r'(?:UE|MME|AMF|SGSN)', flow_text)
                actor = actors[0] if actors else None
                
                # Extract conditions if any
                conditions = self.extract_conditions(context)
                
                flow_step = {
                    'step_number': step_number,
                    'description': flow_text,
                    'context': context,
                    'actor': actor,
                    'conditions': conditions,
                    'source_spec': spec_info.get('source'),
                    'section': spec_info.get('section')
                }
                
                flow_steps.append(flow_step)
                step_number += 1
        
        return flow_steps

    def extract_metadata(self, text: str, spec_info: Dict) -> Dict:
        """Extract metadata information"""
        metadata = {
            'message_types': [],
            'protocol_info': [],
            'timers': [],
            'identifiers': [],
            'cause_values': [],
            'version_info': []
        }
        
        for pattern in self.patterns['METADATA']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                metadata_text = match.group().strip()
                
                # Categorize metadata
                if 'Message Type' in metadata_text:
                    metadata['message_types'].append(metadata_text)
                elif 'Protocol' in metadata_text:
                    metadata['protocol_info'].append(metadata_text)
                elif any(timer in metadata_text for timer in ['T3410', 'T3411', 'T3421', 'T3440', 'T3450']):
                    metadata['timers'].append(metadata_text)
                elif any(id_type in metadata_text for id_type in ['Message ID', 'Sequence Number', 'Transaction ID']):
                    metadata['identifiers'].append(metadata_text)
                elif 'Cause' in metadata_text:
                    metadata['cause_values'].append(metadata_text)
                elif 'Version' in metadata_text:
                    metadata['version_info'].append(metadata_text)
        
        return metadata

    def extract_attach_flow(self, text: str) -> List[Dict]:
        """Extract Attach procedure specific flow with enhanced sequence tracking"""
        flow_steps = []
        step_number = 1
        
        # Define the expected flow patterns with sequence information
        flow_patterns = [
            (r'(?:UE|MS)\s+(?:in|enters?)\s+EMM-DEREGISTERED', 'Initial State', 1),
            (r'(?:UE|MS)\s+sends?\s+ATTACH\s+REQUEST', 'Attach Request', 2),
            (r'MME\s+(?:initiates?|starts?)\s+authentication', 'Authentication', 3),
            (r'MME\s+sends?\s+SECURITY\s+MODE\s+COMMAND', 'Security Mode', 4),
            (r'MME\s+sends?\s+ATTACH\s+ACCEPT', 'Attach Accept', 5),
            (r'(?:UE|MS)\s+sends?\s+ATTACH\s+COMPLETE', 'Attach Complete', 6),
            (r'(?:UE|MS)\s+(?:in|enters?)\s+EMM-REGISTERED', 'Final State', 7)
        ]
        
        for pattern, step_type, sequence in flow_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Extract actors
                actor = 'UE' if any(ue in match.group().upper() for ue in ['UE', 'MS']) else 'MME'
                
                # Extract conditions and parameters
                conditions = self.extract_conditions(context)
                parameters = self.extract_attach_parameters(context)
                
                # Extract metadata
                metadata = self.extract_metadata(context, {})
                
                flow_step = {
                    'step_number': sequence,
                    'type': step_type,
                    'description': match.group().strip(),
                    'actor': actor,
                    'context': context,
                    'conditions': conditions,
                    'parameters': parameters,
                    'metadata': metadata
                }
                
                flow_steps.append(flow_step)
        
        # Sort steps based on sequence
        flow_steps.sort(key=lambda x: x['step_number'])
        
        return flow_steps

    def extract_attach_parameters(self, text: str) -> List[Parameter]:
        """Extract Attach procedure specific parameters"""
        parameters = []
        
        for pattern in self.attach_patterns['parameters']:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                param_text = match.group().strip()
                
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Determine parameter type
                param_type = 'Unknown'
                if any(id_type in param_text.lower() for id_type in ['imsi', 'guti', 'tmsi']):
                    param_type = 'Identity'
                elif 'security' in param_text.lower() or any(sec in param_text.upper() for sec in ['KSI', 'NAS-MAC', 'RAND']):
                    param_type = 'Security'
                elif 'capability' in param_text.lower():
                    param_type = 'Capability'
                elif 'bearer' in param_text.lower():
                    param_type = 'Bearer'
                
                # Check if parameter is mandatory
                mandatory = 'mandatory' in context.lower() or 'shall' in context.lower()
                
                parameter = Parameter(
                    name=param_text,
                    type=param_type,
                    description=context,
                    mandatory=mandatory
                )
                
                # Avoid duplicates
                if not any(p.name == parameter.name for p in parameters):
                    parameters.append(parameter)
        
        return parameters

class Neo4jProtocolStore:
    def __init__(self, uri, user, password):
        try:
            console.print(f"[yellow]Attempting to connect to Neo4j at {uri} with user {user}[/yellow]")
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test the connection
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                result.single()
            console.print("[green]Successfully connected to Neo4j[/green]")
        except Exception as e:
            console.print(f"[red]Failed to connect to Neo4j: {str(e)}[/red]")
            raise

    def batch_store_all(self, tx, all_entities: Dict):
        """Store all entities in a single transaction"""
        # Store states
        if all_entities['states']:
            states_data = [{
                "name": state.name,
                "type": state.type.value if hasattr(state.type, 'value') else state.type,
                "description": state.description[:500],  # Limit description length
                "source_spec": state.source_spec,
                "section": state.section
            } for state in all_entities['states']]
            
            tx.run("""
            UNWIND $states as state
            MERGE (s:State {name: state.name})
            ON CREATE SET 
                s.type = state.type,
                s.description = state.description,
                s.source_spec = state.source_spec,
                s.section = state.section
            """, states=states_data)

        # Store actions
        if all_entities['actions']:
            actions_data = [{
                "name": action.name,
                "actor": action.actor,
                "description": action.description[:500],
                "source_spec": action.source_spec,
                "section": action.section
            } for action in all_entities['actions']]
            
            tx.run("""
            UNWIND $actions as action
            MERGE (a:Action {name: action.name, actor: action.actor})
            ON CREATE SET 
                a.description = action.description,
                a.source_spec = action.source_spec,
                a.section = action.section
            """, actions=actions_data)

        # Store events
        if all_entities['events']:
            events_data = [{
                "name": event.name,
                "trigger": event.trigger,
                "description": event.description[:500],
                "source_spec": event.source_spec,
                "section": event.section
            } for event in all_entities['events']]
            
            tx.run("""
            UNWIND $events as event
            MERGE (e:Event {name: event.name})
            ON CREATE SET 
                e.trigger = event.trigger,
                e.description = event.description,
                e.source_spec = event.source_spec,
                e.section = event.section
            """, events=events_data)

        # Store parameters
        if all_entities['parameters']:
            params_data = [{
                "name": param.name,
                "type": param.type,
                "description": param.description[:500],
                "source_spec": param.source_spec,
                "section": param.section
            } for param in all_entities['parameters']]
            
            tx.run("""
            UNWIND $params as param
            MERGE (p:Parameter {name: param.name})
            ON CREATE SET 
                p.type = param.type,
                p.description = param.description,
                p.source_spec = param.source_spec,
                p.section = param.section
            """, params=params_data)

    def close(self):
        self.driver.close()

    def generate_mermaid_diagram(self, limit: int = 50) -> str:
        """Generate a Mermaid diagram from the stored graph data"""
        mermaid_code = ["graph TD"]
        
        with self.driver.session() as session:
            # Get states and their relationships
            result = session.run("""
            MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
            RETURN s1.name as source, s2.name as target, r.description as label
            LIMIT $limit
            """, limit=limit)
            
            # Add state transitions
            for record in result:
                source = record["source"].replace(" ", "_")
                target = record["target"].replace(" ", "_")
                mermaid_code.append(f"    {source}[{record['source']}] --> {target}[{record['target']}]")
            
            # Get actions and their triggered events
            result = session.run("""
            MATCH (a:Action)-[r:TRIGGERS]->(e:Event)
            RETURN a.name as source, e.name as target, a.actor as actor
            LIMIT $limit
            """, limit=limit)
            
            # Add action-event relationships
            for record in result:
                source = record["source"].replace(" ", "_")
                target = record["target"].replace(" ", "_")
                actor = record["actor"]
                mermaid_code.append(f"    {source}[{record['source']}] -->|{actor}| {target}[{record['target']}]")
            
            # Get events and their impacted states
            result = session.run("""
            MATCH (e:Event)-[r:IMPACTS]->(s:State)
            RETURN e.name as source, s.name as target
            LIMIT $limit
            """, limit=limit)
            
            # Add event-state relationships
            for record in result:
                source = record["source"].replace(" ", "_")
                target = record["target"].replace(" ", "_")
                mermaid_code.append(f"    {source}[{record['source']}] -.->|impacts| {target}[{record['target']}]")
        
        return "\n".join(mermaid_code)

    def export_mermaid_diagram(self, output_file: str = "protocol_diagram.md"):
        """Export the Mermaid diagram to a markdown file"""
        mermaid_code = self.generate_mermaid_diagram()
        
        with open(output_file, "w") as f:
            f.write("# 3GPP Protocol State Diagram\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_code)
            f.write("\n```")
        
        log_progress(f"Mermaid diagram exported to {output_file}")

    def setup_neo4j_schema(self):
        """Setup Neo4j schema with constraints and indexes"""
        with self.driver.session() as session:
            # Create constraints
            constraints = [
                # State constraints
                "CREATE CONSTRAINT state_name IF NOT EXISTS FOR (s:State) REQUIRE s.name IS UNIQUE",
                "CREATE CONSTRAINT state_type IF NOT EXISTS FOR (s:State) REQUIRE s.type IS NOT NULL",
                
                # Event constraints
                "CREATE CONSTRAINT event_name IF NOT EXISTS FOR (e:Event) REQUIRE e.name IS UNIQUE",
                "CREATE CONSTRAINT event_trigger IF NOT EXISTS FOR (e:Event) REQUIRE e.trigger IS NOT NULL",
                
                # Parameter constraints
                "CREATE CONSTRAINT param_name IF NOT EXISTS FOR (p:Parameter) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT param_type IF NOT EXISTS FOR (p:Parameter) REQUIRE p.type IS NOT NULL",
                
                # Action constraints
                "CREATE CONSTRAINT action_name IF NOT EXISTS FOR (a:Action) REQUIRE (a.name, a.actor) IS UNIQUE"
            ]
            
            # Create indexes
            indexes = [
                "CREATE INDEX state_idx IF NOT EXISTS FOR (s:State) ON (s.type)",
                "CREATE INDEX event_idx IF NOT EXISTS FOR (e:Event) ON (e.trigger)",
                "CREATE INDEX param_idx IF NOT EXISTS FOR (p:Parameter) ON (p.type)",
                "CREATE INDEX action_idx IF NOT EXISTS FOR (a:Action) ON (a.actor)"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not create constraint: {str(e)}[/yellow]")
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not create index: {str(e)}[/yellow]")

    def store_attach_procedure(self, data: Dict):
        """Store Attach procedure specific data"""
        with self.driver.session() as session:
            # Store nodes and relationships in separate transactions
            session.execute_write(self._create_attach_nodes, data)
            session.execute_write(self._create_attach_relationships, data)

    def _create_attach_nodes(self, tx, data: Dict):
        """Create nodes for Attach procedure"""
        # Create State nodes
        if data.get('states'):
            tx.run("""
            UNWIND $states as state
            MERGE (s:State {name: state.name})
            SET s.type = state.type,
                s.description = state.description,
                s.conditions = state.conditions
            """, states=data['states'])

        # Create Event nodes
        if data.get('events'):
            tx.run("""
            UNWIND $events as event
            MERGE (e:Event {name: event.name})
            SET e.trigger = event.trigger,
                e.description = event.description
            """, events=data['events'])

        # Create Parameter nodes
        if data.get('parameters'):
            tx.run("""
            UNWIND $parameters as param
            MERGE (p:Parameter {name: param.name})
            SET p.type = param.type,
                p.description = param.description,
                p.mandatory = param.mandatory
            """, parameters=data['parameters'])

    def _create_attach_relationships(self, tx, data: Dict):
        """Create relationships for Attach procedure with enhanced properties"""
        # Create State transitions with conditions
        if data.get('flow'):
            tx.run("""
            UNWIND $steps as step
            MATCH (s1:State {name: step.from_state})
            MATCH (s2:State {name: step.to_state})
            MERGE (s1)-[r:TRANSITIONS_TO {
                sequence: step.step_number,
                description: step.description,
                conditions: step.conditions,
                metadata: step.metadata
            }]->(s2)
            """, steps=data['flow'])

        # Create Action-Event relationships with parameters
        if data.get('actions'):
            tx.run("""
            UNWIND $actions as action
            MATCH (e:Event {name: action.triggers})
            MERGE (a:Action {
                name: action.name,
                actor: action.actor
            })
            MERGE (a)-[r:TRIGGERS]->(e)
            SET r.description = action.description,
                r.parameters = action.parameters,
                r.conditions = action.conditions,
                r.metadata = action.metadata
            """, actions=data['actions'])

    def generate_attach_diagram(self):
        """Generate Mermaid diagram for Attach procedure with enhanced visualization"""
        with self.driver.session() as session:
            # Query for the complete Attach procedure path
            result = session.run("""
            MATCH path = (start:State {type: 'EMM-DEREGISTERED'})-[r:TRANSITIONS_TO*]->(end:State {type: 'EMM-REGISTERED'})
            UNWIND relationships(path) as rel
            WITH DISTINCT rel, startNode(rel) as s1, endNode(rel) as s2
            RETURN s1.name as from_state, s2.name as to_state, 
                   rel.description as description,
                   rel.conditions as conditions,
                   rel.sequence as sequence,
                   rel.metadata as metadata
            ORDER BY rel.sequence
            """)
            
            # Generate Mermaid diagram with enhanced styling
            mermaid_code = ["graph TD;"]
            mermaid_code.append("    %% Attach Procedure Flow")
            
            # Add nodes and edges with styling
            for record in result:
                from_state = record["from_state"].replace(" ", "_")
                to_state = record["to_state"].replace(" ", "_")
                description = record["description"] if record["description"] else ""
                conditions = record["conditions"] if record["conditions"] else []
                sequence = record["sequence"]
                
                # Style nodes based on state type
                if "DEREGISTERED" in from_state:
                    mermaid_code.append(f"    {from_state}[/{from_state}/]:::initial")
                elif "REGISTERED" in from_state:
                    mermaid_code.append(f"    {from_state}[/{from_state}/]:::final")
                else:
                    mermaid_code.append(f"    {from_state}[/{from_state}/]")
                
                # Add edge with sequence and conditions
                edge_label = f"{sequence}. {description}"
                if conditions:
                    edge_label += f"<br>({', '.join(conditions)})"
                
                mermaid_code.append(f"    {from_state} -->|{edge_label}| {to_state}")
            
            # Add styling
            mermaid_code.append("    %% Styling")
            mermaid_code.append("    classDef initial fill:#f9f,stroke:#333,stroke-width:2px;")
            mermaid_code.append("    classDef final fill:#9f9,stroke:#333,stroke-width:2px;")
            
            return "\n".join(mermaid_code)

def log_progress(message: str):
    """Only log major progress points"""
    if "Processing" in message or "completed" in message.lower() or "finished" in message.lower():
        console.print(f"[bold blue]>>> {message}[/bold blue]")

def process_chunk(chunk: str, spec_info: Dict, extractor: ThreeGPPExtractor) -> Dict:
    """Process a single chunk of text"""
    return extractor.extract_all(chunk, spec_info)

def process_pdfs_and_store():
    """Optimized PDF processing with minimal overhead"""
    try:
        # Check if data directory exists in backend folder
        data_dir = os.path.join("backend", "data")
        if not os.path.exists(data_dir):
            console.print("[red]Error: 'backend/data' directory not found. Creating it...[/red]")
            os.makedirs(data_dir)
            console.print("[yellow]Please place your PDF files in the backend/data directory and run again.[/yellow]")
            return

        # Check if any PDF files exist
        pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        if not pdf_files:
            console.print("[red]Error: No PDF files found in backend/data directory[/red]")
            console.print("[yellow]Please add PDF files to the backend/data directory and run again.[/yellow]")
            return

        console.print(f"[green]Found {len(pdf_files)} PDF files to process[/green]")

        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Processing PDFs...", total=len(pdf_files))
            
            try:
                extractor = ThreeGPPExtractor()
                console.print("[green]Successfully initialized extractor[/green]")
            except Exception as e:
                console.print(f"[red]Error initializing extractor: {str(e)}[/red]")
                return

            try:
                store = Neo4jProtocolStore(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
                console.print("[green]Successfully connected to Neo4j[/green]")
            except Exception as e:
                console.print(f"[red]Error connecting to Neo4j: {str(e)}[/red]")
                return
            
            # Process each document
            for doc_index, filename in enumerate(pdf_files, 1):
                try:
                    file_path = os.path.join(data_dir, filename)
                    console.print(f"[blue]Processing document {doc_index}/{len(pdf_files)}: {filename}[/blue]")
                    
                    # Extract text using pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        # Process in batches of 10 pages
                        batch_size = 10
                        total_pages = len(pdf.pages)
                        
                        for batch_start in range(0, total_pages, batch_size):
                            batch_end = min(batch_start + batch_size, total_pages)
                            text = ""
                            
                            # Extract text from batch of pages
                            for page_num in range(batch_start, batch_end):
                                page = pdf.pages[page_num]
                                text += page.extract_text() + "\n\n"
                            
                            # Process the batch
                            spec_info = {
                                'source': filename,
                                'section': None
                            }
                            
                            # Extract entities
                            result = extractor.extract_all(text, spec_info)
                            if result:
                                # Store entities in Neo4j
                                with store.driver.session() as session:
                                    session.execute_write(store.batch_store_all, result)
                            
                            progress.update(task, advance=batch_size/total_pages)
                    
                    console.print(f"[green]Successfully processed {filename}[/green]")
                    
                except Exception as e:
                    console.print(f"[red]Error processing document {filename}: {str(e)}[/red]")
                    continue
            
            store.close()
            console.print("[green]Processing completed successfully![/green]")
            
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        raise

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Neo4j Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    
    console = Console()
    console.print("[bold blue]Starting 3GPP Attach Procedure Extraction[/bold blue]")
    
    try:
        # Initialize extractor and store
        extractor = ThreeGPPExtractor()
        store = Neo4jProtocolStore(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        
        # Setup Neo4j schema
        console.print("[yellow]Setting up Neo4j schema...[/yellow]")
        store.setup_neo4j_schema()
        
        # Process PDFs
        data_dir = "data"
        pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            console.print("[red]No PDF files found in data directory[/red]")
            exit(1)
            
        console.print(f"[green]Found {len(pdf_files)} PDF files to process[/green]")
        
        for pdf_file in pdf_files:
            file_path = os.path.join(data_dir, pdf_file)
            console.print(f"[cyan]Processing {pdf_file}...[/cyan]")
            
            try:
                with pdfplumber.open(file_path) as pdf:
                    total_pages = len(pdf.pages)
                    console.print(f"[blue]Total pages: {total_pages}[/blue]")
                    
                    # Process in batches of 10 pages
                    batch_size = 10
                    for batch_start in range(0, total_pages, batch_size):
                        batch_end = min(batch_start + batch_size, total_pages)
                        console.print(f"[yellow]Processing pages {batch_start+1} to {batch_end}[/yellow]")
                        
                        text = ""
                        # Extract text from batch of pages
                        for page_num in range(batch_start, batch_end):
                            page = pdf.pages[page_num]
                            text += page.extract_text() + "\n\n"
                        
                        # Process the batch
                        spec_info = {
                            'source': pdf_file,
                            'section': None
                        }
                        
                        # Extract entities
                        extracted_data = extractor.extract_all(text, spec_info)
                        if extracted_data:
                            # Extract attach-specific flow
                            flow_data = extractor.extract_attach_flow(text)
                            if flow_data:
                                extracted_data['flow'] = flow_data
                                console.print(f"[green]Found attach procedure flow in pages {batch_start+1}-{batch_end}[/green]")
                            
                            # Store in Neo4j
                            store.store_attach_procedure(extracted_data)
                
                console.print(f"[green]Successfully processed {pdf_file}[/green]")
                
            except Exception as e:
                console.print(f"[red]Error processing {pdf_file}: {str(e)}[/red]")
                continue
        
        # Generate and save Mermaid diagram
        console.print("[yellow]Generating Mermaid diagram...[/yellow]")
        store.export_mermaid_diagram("attach_procedure.md")
        
        console.print("[bold green]Processing completed![/bold green]")
        
        # Print example queries
        console.print("\n[bold blue]Example Neo4j Queries for Visualization:[/bold blue]")
        console.print("""
        1. View complete Attach procedure flow:
        MATCH path = (start:State {type: 'EMM-DEREGISTERED'})-[*]->(end:State {type: 'EMM-REGISTERED'})
        RETURN path
        
        2. View all parameters used in Attach procedure:
        MATCH (a:Action)-[r:USES_PARAMETER]->(p:Parameter)
        RETURN a, r, p
        
        3. View all events and their triggers:
        MATCH (e:Event)
        RETURN e.name, e.trigger, e.description
        
        4. View state transitions with conditions:
        MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
        RETURN s1.name, r.conditions, s2.name
        """)
    except Exception as e:
        console.print(f"[red]Error during execution: {str(e)}[/red]")
    finally:
        # Close Neo4j connection if it exists
        if 'store' in locals():
            store.driver.close() 