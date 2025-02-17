import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from preprocess_pdfs import (
    read_pdfs_from_directory, 
    semantic_chunk_text,
    is_title_page_content,
    is_toc_content,
    is_index_or_appendix_content,
    sentence_transformer
)
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import logging
from rich.console import Console
from rich.logging import RichHandler
import numpy as np
from datetime import datetime

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

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

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
    conditions: List[str] = None
    source_spec: str = None
    section: str = None

    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []

@dataclass
class Action:
    name: str
    actor: str
    description: str
    parameters: List[str] = None
    prerequisites: List[str] = None
    source_spec: str = None
    section: str = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
        if self.prerequisites is None:
            self.prerequisites = []

@dataclass
class Event:
    name: str
    trigger: str
    description: str
    conditions: List[str] = None
    source_spec: str = None
    section: str = None

    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []

@dataclass
class Parameter:
    name: str
    type: str
    description: str
    mandatory: bool = False
    value_range: str = None
    source_spec: str = None
    section: str = None

class ThreeGPPExtractor:
    def __init__(self):
        # Core patterns for protocol analysis
        self.patterns = {
            'STATE': [
                # UE States
                r'(?:EMM|MM|GMM|PMM|CM|RRC|5GMM)-(?:DEREGISTERED|REGISTERED|IDLE|CONNECTED|NULL)',
                r'(?:EMM|MM|GMM|5GMM)-(?:REGISTERED|DEREGISTERED)\.(?:NORMAL-SERVICE|ATTEMPTING-TO-ATTACH|LIMITED-SERVICE|NO-CELL-AVAILABLE)',
                r'(?:EMM|MM|GMM|5GMM)-(?:REGISTERED)\.(?:NORMAL-SERVICE|UPDATE-NEEDED|ATTEMPTING-TO-UPDATE|LIMITED-SERVICE)',
                r'(?:CONNECTED|IDLE|SUSPENDED)\s+(?:state|mode)',
                # Network Element States
                r'(?:MME|AMF|SGSN|MSC)-(?:CONNECTED|IDLE|ACTIVE|STANDBY)',
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
        
        # Initialize sentence transformer if available
        self.sentence_transformer = sentence_transformer

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
        """Extract all components with improved context awareness and performance"""
        # Skip irrelevant sections early
        if is_title_page_content(text) or is_toc_content(text) or is_index_or_appendix_content(text):
            return None
        
        # Extract section context if available
        section_context = self.extract_section_context(text)
        if section_context:
            spec_info['section'] = section_context['section']
        
        # Extract all components with early filtering
        states = []
        actions = []
        events = []
        parameters = []
        conditions = []
        
        # Only process text chunks that are likely to contain relevant information
        relevant_text = text
        if "attach" in text.lower():
            # Extract states
            states = self.extract_states(relevant_text, spec_info)
            
            # Extract actions only if we found states
            if states:
                actions = self.extract_actions(relevant_text, spec_info)
                
                # Extract events only if we found actions
                if actions:
                    events = self.extract_events(relevant_text, spec_info)
                    
                    # Extract parameters only if we found events
                    if events:
                        parameters = self.extract_parameters(relevant_text, spec_info)
                        conditions = self.extract_conditions(relevant_text)
        
        return {
            'states': states,
            'actions': actions,
            'events': events,
            'parameters': parameters,
            'conditions': conditions,
            'source': spec_info.get('source'),
            'section': spec_info.get('section')
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

class Neo4jProtocolStore:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.sentence_transformer = sentence_transformer
        self.batch_size = 100  # Add batch size parameter

    def batch_store_states(self, tx, states: List[State]):
        """Store states in batches"""
        query = """
        UNWIND $states as state
        MERGE (s:State {name: state.name, type: state.type})
        ON CREATE SET 
            s.description = state.description,
            s.source_spec = state.source_spec,
            s.section = state.section
        """
        states_data = [{
            "name": state.name,
            "type": state.type.value,
            "description": state.description,
            "source_spec": state.source_spec,
            "section": state.section
        } for state in states]
        
        tx.run(query, states=states_data)

        # Batch store conditions
        conditions_data = []
        for state in states:
            for condition in state.conditions:
                conditions_data.append({
                    "condition": condition,
                    "state_name": state.name
                })
        
        if conditions_data:
            tx.run("""
            UNWIND $conditions as cond
            MERGE (c:Condition {text: cond.condition})
            WITH c, cond
            MATCH (s:State {name: cond.state_name})
            MERGE (s)-[:HAS_CONDITION]->(c)
            """, conditions=conditions_data)

    def batch_store_actions(self, tx, actions: List[Action]):
        """Store actions in batches"""
        query = """
        UNWIND $actions as action
        MERGE (a:Action {name: action.name, actor: action.actor})
        ON CREATE SET 
            a.description = action.description,
            a.source_spec = action.source_spec,
            a.section = action.section
        """
        actions_data = [{
            "name": action.name,
            "actor": action.actor,
            "description": action.description,
            "source_spec": action.source_spec,
            "section": action.section
        } for action in actions]
        
        tx.run(query, actions=actions_data)

        # Batch store parameters
        params_data = []
        for action in actions:
            for param in action.parameters:
                param_name = param.name if isinstance(param, Parameter) else str(param)
                params_data.append({
                    "param": param_name,
                    "action_name": action.name
                })
        
        if params_data:
            tx.run("""
            UNWIND $params as param
            MERGE (p:Parameter {name: param.param})
            WITH p, param
            MATCH (a:Action {name: param.action_name})
            MERGE (a)-[:USES_PARAMETER]->(p)
            """, params=params_data)

    def batch_store_events(self, tx, events: List[Event]):
        """Store events in batches"""
        query = """
        UNWIND $events as event
        MERGE (e:Event {name: event.name, trigger: event.trigger})
        ON CREATE SET 
            e.description = event.description,
            e.source_spec = event.source_spec,
            e.section = event.section
        """
        events_data = [{
            "name": event.name,
            "trigger": event.trigger,
            "description": event.description,
            "source_spec": event.source_spec,
            "section": event.section
        } for event in events]
        
        tx.run(query, events=events_data)

    def batch_store_parameters(self, tx, parameters: List[Parameter]):
        """Store parameters in batches"""
        query = """
        UNWIND $parameters as param
        MERGE (p:Parameter {name: param.name, type: param.type})
        ON CREATE SET 
            p.description = param.description,
            p.mandatory = param.mandatory,
            p.value_range = param.value_range,
            p.source_spec = param.source_spec,
            p.section = param.section
        """
        params_data = [{
            "name": param.name,
            "type": param.type,
            "description": param.description,
            "mandatory": param.mandatory,
            "value_range": param.value_range,
            "source_spec": param.source_spec,
            "section": param.section
        } for param in parameters]
        
        tx.run(query, parameters=params_data)

    def batch_create_relationships(self, tx, results: Dict):
        """Create relationships in batches with optimized queries"""
        def calculate_confidence(text1: str, text2: str) -> float:
            """Calculate confidence score between two text descriptions"""
            if self.sentence_transformer:
                try:
                    emb1 = self.sentence_transformer.encode(text1, show_progress_bar=False)
                    emb2 = self.sentence_transformer.encode(text2, show_progress_bar=False)
                    return float(np.dot(emb1, emb2))
                except:
                    return 0.5
            return 0.5

        # Process only high-confidence relationships
        MIN_CONFIDENCE = 0.7  # Increase confidence threshold
        MAX_RELATIONSHIPS = 1000  # Limit number of relationships
        
        # Create relationships in batches
        relationships = []
        relationship_count = 0
        
        # Process state transitions with limits
        for state1 in results['states'][:MAX_RELATIONSHIPS]:
            for state2 in results['states'][:MAX_RELATIONSHIPS]:
                if state1 != state2 and state1.section == state2.section:
                    confidence = calculate_confidence(state1.description, state2.description)
                    if confidence > MIN_CONFIDENCE:
                        relationships.append({
                            "from_state": state1.name,
                            "to_state": state2.name,
                            "type": "TRANSITIONS_TO",
                            "confidence": confidence,
                            "conditions": [str(c) for c in state1.conditions]
                        })
                        relationship_count += 1
                        
                        if relationship_count >= MAX_RELATIONSHIPS:
                            break
            if relationship_count >= MAX_RELATIONSHIPS:
                break
        
        # Batch create all relationships at once
        if relationships:
            tx.run("""
            UNWIND $rels as rel
            MATCH (from {name: rel.from_state}), (to {name: rel.to_state})
            MERGE (from)-[r:rel.type]->(to)
            SET r += {
                confidence: rel.confidence,
                conditions: rel.conditions
            }
            """, rels=relationships)

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

def log_progress(message: str):
    """Only log major progress points"""
    if "Processing" in message or "completed" in message.lower() or "finished" in message.lower():
        console.print(f"[bold blue]>>> {message}[/bold blue]")

def process_pdfs_and_store():
    """Process PDFs and store extracted information in Neo4j with optimized batch processing"""
    try:
        extractor = ThreeGPPExtractor()
        store = Neo4jProtocolStore(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        
        log_progress("Reading PDFs from data directory...")
        documents = read_pdfs_from_directory("data")
        
        if not documents:
            console.print("[yellow]Warning: No documents found in data directory[/yellow]")
            return
        
        total_docs = len(documents)
        log_progress(f"Processing {total_docs} documents...")
        
        # Collect all entities before batch storing
        all_states = []
        all_actions = []
        all_events = []
        all_parameters = []
        
        # Process documents in smaller chunks
        MAX_CHUNK_SIZE = 2000  # Reduce chunk size for faster processing
        BATCH_SIZE = 50  # Smaller batch size for more frequent updates
        
        for doc in documents:
            spec_info = {
                'source': doc.get('metadata', {}).get('source', 'Unknown'),
                'section': None
            }
            
            # Split text into smaller chunks
            chunks = semantic_chunk_text(doc['text'], max_chunk_size=MAX_CHUNK_SIZE)
            
            # Process chunks in parallel
            for chunk in chunks:
                # Skip irrelevant sections early
                if is_title_page_content(chunk) or is_toc_content(chunk) or is_index_or_appendix_content(chunk):
                    continue
                    
                # Focus on sections containing "Attach procedure"
                if "attach procedure" not in chunk.lower():
                    continue
                
                results = extractor.extract_all(chunk, spec_info)
                if results:
                    all_states.extend(results['states'])
                    all_actions.extend(results['actions'])
                    all_events.extend(results['events'])
                    all_parameters.extend(results['parameters'])
                
                # Process in smaller batches to avoid memory issues
                if len(all_states) >= BATCH_SIZE:
                    with store.driver.session() as session:
                        session.execute_write(store.batch_store_states, all_states[:BATCH_SIZE])
                    all_states = all_states[BATCH_SIZE:]
                
                if len(all_actions) >= BATCH_SIZE:
                    with store.driver.session() as session:
                        session.execute_write(store.batch_store_actions, all_actions[:BATCH_SIZE])
                    all_actions = all_actions[BATCH_SIZE:]
                
                if len(all_events) >= BATCH_SIZE:
                    with store.driver.session() as session:
                        session.execute_write(store.batch_store_events, all_events[:BATCH_SIZE])
                    all_events = all_events[BATCH_SIZE:]
                
                if len(all_parameters) >= BATCH_SIZE:
                    with store.driver.session() as session:
                        session.execute_write(store.batch_store_parameters, all_parameters[:BATCH_SIZE])
                    all_parameters = all_parameters[BATCH_SIZE:]
        
        # Store remaining entities
        with store.driver.session() as session:
            if all_states:
                session.execute_write(store.batch_store_states, all_states)
            if all_actions:
                session.execute_write(store.batch_store_actions, all_actions)
            if all_events:
                session.execute_write(store.batch_store_events, all_events)
            if all_parameters:
                session.execute_write(store.batch_store_parameters, all_parameters)
            
            # Create relationships in smaller batches
            for i in range(0, len(all_states), BATCH_SIZE):
                batch_states = all_states[i:i + BATCH_SIZE]
                session.execute_write(store.batch_create_relationships, {
                    'states': batch_states,
                    'actions': all_actions,
                    'events': all_events,
                    'parameters': all_parameters
                })
        
        log_progress("All documents processed successfully!")
        store.close()
        
        # Generate and export Mermaid diagram
        store = Neo4jProtocolStore(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        store.export_mermaid_diagram()
        store.close()
        
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        raise

if __name__ == "__main__":
    console.print("[bold blue]" + "=" * 80 + "[/bold blue]")
    console.print("[bold blue]3GPP PROTOCOL EXTRACTION AND STORAGE[/bold blue]")
    console.print("[bold blue]" + "=" * 80 + "[/bold blue]")
    
    try:
        process_pdfs_and_store()
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
    
    console.print("[bold blue]" + "=" * 80 + "[/bold blue]") 