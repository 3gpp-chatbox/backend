import os
import re
import json
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Any, Set, Optional, Literal
from dotenv import load_dotenv
from rich.console import Console
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential
import traceback
from pathlib import Path
from pipeline.semantic_chunking import SemanticChunker, save_semantic_chunks
from models import RegistrationAnalysis, NetworkElement, State, RegistrationStep, Metadata
from models import RegistrationData, NetworkElement, ProcedureStep, Procedure
from pydantic import ValidationError, BaseModel, Field, validator
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize console for better output
console = Console()

# Load environment variables
load_dotenv(override=True)

# Configuration
INPUT_MD_FILE = os.path.join("processed_data", "semantic_TS_24.501.md")
PROCESSED_DATA_FOLDER = os.path.join("processed_data")
LLM_MODEL = "gemini-2.0-flash"
OUTPUT_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.json")
OUTPUT_MD_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.md")
INTERMEDIATE_BATCH_SIZE = 10
RATE_LIMIT_DELAY = 1
MAX_RETRIES = 3

EXTRACTION_PROMPT = '''You are an expert in 5G NAS signaling procedures as defined in 3GPP TS 24.501. Your task is to extract the complete execution flow of the Initial Registration Procedure for each trigger and return it as structured JSON data for visualization.

For each trigger of the Initial Registration Procedure, you must provide:
1. Network Elements involved (UE, gNB, AMF, etc.)
2. States that the system goes through
3. Events that occur during the procedure
4. Edges connecting states and events

The output should follow this exact structure:
{
  "procedure": "Initial Registration",
  "trigger": "<TRIGGER_NAME>",
  "nodes": [
    // Network Elements (at least 3)
    { "id": "N1", "label": "User Equipment (UE)", "type": "NetworkElement" },
    { "id": "N2", "label": "gNB (gNodeB)", "type": "NetworkElement" },
    { "id": "N3", "label": "AMF", "type": "NetworkElement" },

    // States (at least 4)
    { "id": "S1", "label": "Initial State", "type": "State" },
    { "id": "S2", "label": "Intermediate State", "type": "State" },
    // ... more states ...

    // Events (at least 3)
    { "id": "E1", "label": "Event Description", "type": "Event" },
    { "id": "E2", "label": "Event Description", "type": "Event" }
    // ... more events ...
  ],
  "edges": [
    { "from": "N1", "to": "N2", "label": "Description of transition" },
    { "from": "N2", "to": "N3", "label": "Description of transition" },
    { "from": "N3", "to": "S1", "label": "Description of transition" },
    { "from": "S1", "to": "E1", "label": "Description of transition" },
    { "from": "E1", "to": "S2", "label": "Description of transition" },
    { "from": "S2", "to": "E2", "label": "Description of transition" },
    { "from": "E2", "to": "S3", "label": "Description of transition" },
    { "from": "S3", "to": "N4", "label": "Description of transition" },
    
  ],
  "metadata": {
    "procedureName": "Initial Registration",
    "specReference": "3GPP TS 24.501",
    "protocol": "5G NAS",
    "trigger": "<TRIGGER_NAME>",
    "mandatoryMessages": [
      "Registration Request",
      "Registration Accept",
      "Registration Complete"
    ]
  }
}

Initial Registration Triggers to extract:
1. Power On / UE Startup
2. Enter 5G Coverage
3. Change of PLMN
4. Change in Subscription
5. Registration Area Change
6. Loss of Connection
7. Explicit Deregistration
8. Security Context Change
9. Emergency Registration

Requirements:
1. Each node must have a unique ID (N1, N2... for NetworkElements, S1, S2... for States, E1, E2... for Events)
2. All edges must connect existing nodes
3. The flow must be complete from initial state to final registered state
4. Include all mandatory NAS messages in the flow
5. Include security and authentication steps
6. Edges must accurately describe the transition or message being sent

Extract the complete flow for the given text, ensuring all requirements are met.'''

# Initial Registration Triggers
INITIAL_REGISTRATION_TRIGGERS = {
    "Power On / UE Startup": [
        r"power.*on",
        r"UE.*startup",
        r"first.*time.*register",
        r"initial.*power.*on"
    ],
    "Enter 5G Coverage": [
        r"enter.*5G.*coverage",
        r"move.*into.*5G",
        r"non-5G.*to.*5G",
        r"5G.*coverage.*area"
    ],
    "Change of PLMN": [
        r"change.*PLMN",
        r"new.*PLMN",
        r"different.*PLMN",
        r"PLMN.*change"
    ],
    "Change in Subscription": [
        r"subscription.*change",
        r"USIM.*update",
        r"subscription.*information",
        r"subscription.*data"
    ],
    "Registration Area Change": [
        r"tracking.*area.*update.*fail",
        r"TAU.*reject",
        r"registration.*area.*change",
        r"area.*update.*failure"
    ],
    "Loss of Connection": [
        r"deregister.*AMF",
        r"connection.*loss",
        r"inactivity",
        r"registration.*timer.*expir"
    ],
    "Explicit Deregistration": [
        r"5GMM.*De-registration",
        r"explicit.*deregister",
        r"UE.*deregister",
        r"voluntary.*deregister"
    ],
    "Security Context Change": [
        r"security.*context.*lost",
        r"NAS.*security.*reset",
        r"security.*parameter.*change",
        r"fresh.*security"
    ],
    "Emergency Registration": [
        r"emergency.*call",
        r"emergency.*registration",
        r"emergency.*service",
        r"emergency.*PDU"
    ]
}

RELEVANT_KEYWORDS = [
    "registration procedure", 
    "5GMM",
    "initial registration",
    "UE registration",
    "AMF",
    "SMF",
    "registration accept",
    "registration request",
    "5GMM-REGISTERED",
    "5GMM-DEREGISTERED",
    "REGISTRATION ACCEPT",
    "REGISTRATION REQUEST",
    
    # Initial registration specific keywords
    "power on",
    "startup",
    "5G coverage",
    "PLMN",
    "subscription",
    "tracking area",
    "deregistration",
    "security context",
    "emergency",
    
    # Additional trigger-related keywords
    "trigger",
    "initiated by",
    "caused by",
    "when",
    "if",
    "condition",
    "requirement",
    "prerequisite",
    "start",
    "begin",
    "initiate"
]

class ValidatedData:
    def __init__(self, data: RegistrationData):
        self.data = data
        self.validation_timestamp = datetime.now()
        self.is_validated = True

class Node(BaseModel):
    id: str
    label: str
    type: Literal["NetworkElement", "State", "Event"]

class Edge(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    label: str

class Metadata(BaseModel):
    procedureName: str
    specReference: str
    protocol: str
    trigger: str
    mandatoryMessages: List[str]

class RegistrationProcedure(BaseModel):
    procedure: str
    trigger: str
    nodes: List[Node]
    edges: List[Edge]
    metadata: Metadata

    @validator("nodes")
    def validate_node_types(cls, nodes):
        network_elements = [n for n in nodes if n.type == "NetworkElement"]
        states = [n for n in nodes if n.type == "State"]
        events = [n for n in nodes if n.type == "Event"]
        
        if len(network_elements) < 2:
            raise ValueError("Must have at least 2 network elements")
        if len(states) < 4:
            raise ValueError("Must have at least 4 states")
        if len(events) < 3:
            raise ValueError("Must have at least 3 events")
        return nodes

    @validator("edges")
    def validate_edge_connections(cls, edges, values):
        if "nodes" not in values:
            return edges
            
        node_ids = {n.id for n in values["nodes"]}
        for edge in edges:
            if edge.from_ not in node_ids:
                raise ValueError(f"Edge from node {edge.from_} does not exist")
            if edge.to not in node_ids:
                raise ValueError(f"Edge to node {edge.to} does not exist")
        return edges

class ExtractionResult(BaseModel):
    procedures: List[RegistrationProcedure]
    extraction_timestamp: datetime = Field(default_factory=datetime.now)
    total_procedures: int = Field(0)
    successful_extractions: int = Field(0)

def initialize_llm():
    """Initialize LLM with error handling."""
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("Missing Google API key. Please check your .env file.")

        console.print(f"[blue]Using Google Gemini: {LLM_MODEL}[/blue]")
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=0,
            max_output_tokens=2048
        )
        return llm

    except Exception as e:
        console.print(f"[red]Error initializing LLM: {str(e)}[/red]")
        raise

def ensure_folders_exist():
    """Create necessary folders if they don't exist."""
    folders = [
        PROCESSED_DATA_FOLDER
    ]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        console.print(f"[blue]Ensuring folder exists: {folder}[/blue]")

def save_completion_marker():
    """Save a marker file to indicate completion of processing."""
    try:
        marker_file = os.path.join(PROCESSED_DATA_FOLDER, "extraction_complete.json")
        completion_data = {
            "timestamp": datetime.now().isoformat(),
            "status": "complete"
        }
        with open(marker_file, 'w') as f:
            json.dump(completion_data, f, indent=2)
        console.print(f"[green]✓ Saved completion marker to {marker_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving completion marker: {str(e)}[/red]")

def process_md_chunks(md_file_path: str, llm) -> List[Dict]:
    """Process semantic chunks from markdown file."""
    try:
        console.print(f"\n[blue]Starting extraction process...[/blue]")
        console.print(f"[blue]Reading from: {md_file_path}[/blue]")
        
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # Debug: Show file content
        console.print(f"\n[yellow]File size: {len(md_content)} characters[/yellow]")
        console.print("[yellow]First 200 characters of content:[/yellow]")
        console.print(md_content[:200])

        # Split chunks
        chunks = md_content.split("## Semantic Chunk")[1:]
        console.print(f"\n[blue]Found {len(chunks)} chunks[/blue]")
        
        # Debug: Show first chunk
        if chunks:
            console.print("\n[yellow]First chunk preview:[/yellow]")
            console.print(chunks[0][:200])
            
            # Check for relevant keywords
            console.print("\n[blue]Checking keywords in first chunk:[/blue]")
            for keyword in RELEVANT_KEYWORDS:
                if keyword.lower() in chunks[0].lower():
                    console.print(f"[green]Found keyword: {keyword}[/green]")

        results = []
        for chunk_index, chunk in enumerate(chunks):
            console.print(f"\n[blue]Processing chunk {chunk_index + 1}/{len(chunks)}[/blue]")
            doc = Document(page_content=chunk, metadata={
                "source": md_file_path,
                "chunk_index": chunk_index,
                "total_chunks": len(chunks)
            })
            
            # Check if chunk is relevant
            if not is_relevant_chunk(doc.page_content):
                console.print("[yellow]Skipping irrelevant chunk[/yellow]")
                continue
                
            console.print("[green]Processing relevant chunk...[/green]")
            chunk_result = process_chunk(doc, llm)
            if chunk_result:
                results.append(chunk_result)
                console.print("[green]Successfully extracted data from chunk[/green]")

        console.print(f"\n[blue]Extraction complete. Found {len(results)} relevant results[/blue]")
        return results

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return []

def validate_llm_output(data: dict) -> Optional[ValidatedData]:
    """Validate LLM output and clean data if needed"""
    try:
        # Define valid initial registration triggers
        VALID_TRIGGERS = {
            "Power On / UE Startup",
            "Enter 5G Coverage",
            "Change of PLMN",
            "Change in Subscription",
            "Registration Area Change",
            "Loss of Connection",
            "Explicit Deregistration",
            "Security Context Change",
            "Emergency Registration"
        }

        # Define valid message types
        VALID_MESSAGE_TYPES = {
            # Required messages
            "Registration Request",
            "Authentication Request",
            "Authentication Vector Request",
            "Authentication Response",
            "Security Mode Command",
            "Security Mode Complete",
            "Registration Accept",
            "Registration Complete",
            # Optional messages
            "Registration Reject",
            "Identity Request",
            "Identity Response",
            "DL NAS Transport",
            "UL NAS Transport"
        }

        # Check existing nodes for required messages
        required_messages = {
            "Registration Request": False,
            "Authentication Request": False,
            "Authentication Vector Request": False,
            "Authentication Response": False,
            "Security Mode Command": False,
            "Security Mode Complete": False,
            "Registration Accept": False,
            "Registration Complete": False
        }
        
        existing_nodes = data.get("nodes", [])
        
        # First pass: check existing messages
        for node in existing_nodes:
            msg_type = node.get("messageType", "")
            if msg_type in required_messages:
                required_messages[msg_type] = True

        # Initialize nodes if empty or missing required messages
        if not existing_nodes or not all(required_messages.values()):
            if not existing_nodes:
                data["nodes"] = []
            
            # Add missing mandatory messages while preserving existing ones
            message_sequence = [
                ("Registration Request", "UE", "AMF"),
                ("Authentication Request", "AMF", "UE"),
                ("Authentication Vector Request", "AUSF", "UDM"),
                ("Authentication Response", "UE", "AMF"),
                ("Security Mode Command", "AMF", "UE"),
                ("Security Mode Complete", "UE", "AMF"),
                ("Registration Accept", "AMF", "UE"),
                ("Registration Complete", "UE", "AMF")
            ]
            
            for i, (msg_type, source, target) in enumerate(message_sequence):
                if not required_messages.get(msg_type, True):
                    data["nodes"].append({
                        "id": f"A{i + 1}",
                        "label": f"{source} sends {msg_type}",
                        "messageType": msg_type,
                        "source": source,
                        "target": target
                    })

        # Validate and clean nodes
        for i, node in enumerate(data["nodes"]):
            # Ensure required fields exist
            if "id" not in node:
                node["id"] = f"A{i + 1}"
            if "label" not in node:
                node["label"] = f"Step {i + 1}"
            if "source" not in node:
                node["source"] = "UE" if "UE" in node["label"] else "AMF"
            if "target" not in node:
                node["target"] = "AMF" if "AMF" in node["label"] else "UE"

        # Generate edges if missing
        if "edges" not in data or not data["edges"]:
            data["edges"] = []
            for i in range(len(data["nodes"]) - 1):
                current_node = data["nodes"][i]
                next_node = data["nodes"][i + 1]
                data["edges"].append({
                    "from": current_node["id"],
                    "to": next_node["id"],
                    "label": f"Step {i+1} to {i+2}"
                })

        # Validate trigger
        if not data.get("trigger") or data["trigger"] not in VALID_TRIGGERS:
            data["trigger"] = "Power On / UE Startup"  # Default trigger

        # Create metadata if not present
        if "metadata" not in data:
            data["metadata"] = {
                "procedureName": "Initial Registration",
                "specReference": "3GPP TS 24.501",
                "protocol": "5G NAS",
                "parameters": {
                    "SUPI": "Extracted if present",
                    "GUTI": "Extracted if present",
                    "5G-GUTI": "Assigned during registration",
                    "SecurityContext": "Established during procedure"
                }
            }

        # Convert to RegistrationData
        validated_data = RegistrationData(
            procedure=Procedure(
                name="Initial Registration",
                description="Complete 5G Initial Registration procedure"
            ),
            network_elements=[
                NetworkElement(name="UE", type="Network Element", description="User Equipment"),
                NetworkElement(name="AMF", type="Network Element", description="Access and Mobility Management Function"),
                NetworkElement(name="AUSF", type="Network Element", description="Authentication Server Function"),
                NetworkElement(name="UDM", type="Network Element", description="Unified Data Management")
            ],
            procedure_flow=[
                ProcedureStep(
                    sequence_number=i+1,
                    source=node["source"],
                    target=node["target"],
                    message=node["label"],
                    description=node.get("description", node["label"]),
                    message_type=node.get("messageType"),
                    conditions=[],
                    timing=None
                ) for i, node in enumerate(data["nodes"])
            ]
        )

        return ValidatedData(validated_data)

    except Exception as e:
        console.print(f"[red]Validation error: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return None

def verify_extraction(data: dict) -> bool:
    """Verify if all required nodes and edges are extracted for initial registration"""
    try:
        # First try to validate using Pydantic model
        try:
            procedure = RegistrationProcedure(**data)
            console.print("[green]✓ Basic structure validation passed[/green]")
        except ValidationError as ve:
            console.print(f"[red]Structure validation failed: {str(ve)}[/red]")
            return False

        # Verify network elements
        network_elements = [n for n in procedure.nodes if n.type == "NetworkElement"]
        required_elements = {"UE", "gNB", "AMF"}
        found_elements = {ne.label.split('(')[0].strip() for ne in network_elements}
        
        missing_elements = required_elements - found_elements
        if missing_elements:
            console.print(f"[red]Missing required network elements: {', '.join(missing_elements)}[/red]")
            return False
        else:
            console.print(f"[green]✓ Found all required network elements: {', '.join(found_elements)}[/green]")

        # Verify states
        states = [n for n in procedure.nodes if n.type == "State"]
        if len(states) < 4:
            console.print(f"[red]Insufficient states: found {len(states)}, need at least 4[/red]")
            return False
        console.print(f"[green]✓ Found {len(states)} states[/green]")

        # Verify events
        events = [n for n in procedure.nodes if n.type == "Event"]
        if len(events) < 3:
            console.print(f"[red]Insufficient events: found {len(events)}, need at least 3[/red]")
            return False
        console.print(f"[green]✓ Found {len(events)} events[/green]")

        # Verify edges connect existing nodes
        node_ids = {n.id for n in procedure.nodes}
        for edge in procedure.edges:
            if edge.from_ not in node_ids:
                console.print(f"[red]Edge references non-existent from node: {edge.from_}[/red]")
                return False
            if edge.to not in node_ids:
                console.print(f"[red]Edge references non-existent to node: {edge.to}[/red]")
                return False

        console.print("[green]✓ All edges reference valid nodes[/green]")

        # Verify mandatory messages in metadata
        required_messages = {
            "Registration Request",
            "Registration Accept",
            "Registration Complete"
        }
        
        found_messages = set(procedure.metadata.mandatoryMessages)
        missing_messages = required_messages - found_messages
        if missing_messages:
            console.print(f"[red]Missing mandatory messages: {', '.join(missing_messages)}[/red]")
            return False
        console.print("[green]✓ All mandatory messages present[/green]")

        # Verify trigger is valid
        valid_triggers = {
            "Power On / UE Startup",
            "Enter 5G Coverage",
            "Change of PLMN",
            "Change in Subscription",
            "Registration Area Change",
            "Loss of Connection",
            "Explicit Deregistration",
            "Security Context Change",
            "Emergency Registration"
        }

        if not any(trigger.lower() in procedure.trigger.lower() for trigger in valid_triggers):
            console.print(f"[red]Invalid trigger: {procedure.trigger}[/red]")
            return False
        console.print(f"[green]✓ Valid trigger: {procedure.trigger}[/green]")

        # All checks passed
        console.print("\n[green]✓ Extraction verification completed successfully[/green]")
        return True

    except Exception as e:
        console.print(f"[red]Error during verification: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return False

def process_chunk(doc: Document, llm: Any) -> Dict:
    try:
        chunk_info = f"Processing chunk {doc.metadata['chunk_index'] + 1}/{doc.metadata['total_chunks']}"
        console.print(f"\n[blue]{chunk_info}[/blue]")
        
        # Debug: Show chunk content preview
        preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        console.print("\n[blue]Chunk content preview:[/blue]")
        console.print(preview)
        
        messages = [
            SystemMessage(content=EXTRACTION_PROMPT),
            HumanMessage(content=f"Extract ALL initial registration triggers and their flows from this text:\n\n{doc.page_content}")
        ]
        
        try:
            # Call LLM
            response = llm.invoke(messages)
            response_text = response.content.strip()
            
            # Debug: Show raw LLM response
            console.print("\n[blue]Raw LLM Response:[/blue]")
            console.print(response_text)
            
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > 0:
                json_str = response_text[json_start:json_end]
                console.print("\n[blue]Attempting to parse JSON[/blue]")
                
                try:
                    # Remove any markdown formatting
                    json_str = re.sub(r'```json\s*|\s*```', '', json_str)
                    json_str = json_str.strip()
                    
                    # Parse the JSON
                    data = json.loads(json_str)
                    
                    # Validate using Pydantic
                    try:
                        # Convert to RegistrationProcedure model
                        procedure = RegistrationProcedure(**data)
                        console.print("[green]✓ Successfully validated registration procedure[/green]")
                        
                        # Return validated data
                        return procedure.model_dump()
                    except ValidationError as ve:
                        console.print(f"[red]Validation error: {str(ve)}[/red]")
                        # Return raw data for debugging
                        return {
                            "error": f"Validation failed: {str(ve)}",
                            "raw_data": data
                        }
                        
                except json.JSONDecodeError as e:
                    console.print(f"[red]JSON Parse Error: {str(e)}[/red]")
                    console.print(f"[yellow]Attempted to parse:[/yellow]\n{json_str[:1000]}...")
                    return {"error": f"JSON parse error: {str(e)}"}
            else:
                console.print("[red]No JSON structure found in response[/red]")
                return {"error": "No JSON found in response"}
                
        except Exception as e:
            console.print(f"[red]Error calling LLM: {str(e)}[/red]")
            console.print(traceback.format_exc())
            return {"error": f"LLM error: {str(e)}"}
            
    except Exception as e:
        console.print(f"[red]Error processing chunk: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return {"error": f"Processing error: {str(e)}"}

def verify_complete_response(data: dict) -> bool:
    """Verify if response contains all required elements including additional triggers"""
    
    # Check basic structure
    required_keys = {"procedure", "nodes", "edges", "metadata"}
    if not all(key in data for key in required_keys):
        console.print("[red]Missing required sections in response[/red]")
        return False
        
    try:
        # Validate using Pydantic model
        procedure = RegistrationProcedure(**data)
        
        # Check network elements (must have all required)
        network_elements = [n for n in procedure.nodes if n.type == "NetworkElement"]
        required_elements = {"UE", "gNB", "AMF"}
        found_elements = {ne.label.split('(')[0].strip() for ne in network_elements}
        if not required_elements.issubset(found_elements):
            console.print(f"[red]Missing network elements: {required_elements - found_elements}[/red]")
            return False
            
        # Check states (must have at least 4)
        states = [n for n in procedure.nodes if n.type == "State"]
        if len(states) < 4:
            console.print("[red]Insufficient states[/red]")
            return False
            
        # Check events (must have at least 3)
        events = [n for n in procedure.nodes if n.type == "Event"]
        if len(events) < 3:
            console.print("[red]Insufficient events[/red]")
            return False
            
        # Check mandatory messages
        required_messages = {
            "Registration Request",
            "Registration Accept",
            "Registration Complete"
        }
        if not required_messages.issubset(set(procedure.metadata.mandatoryMessages)):
            console.print("[red]Missing mandatory messages[/red]")
            return False
            
        # All checks passed
        console.print("[green]✓ Response verification complete - all elements present[/green]")
        return True
        
    except ValidationError as ve:
        console.print(f"[red]Validation error: {str(ve)}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Error during verification: {str(e)}[/red]")
        return False

@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=5),
    reraise=True
)
def call_llm_with_retry(llm: Any, prompt: str) -> Dict:
    """Call LLM with retry logic and rate limiting."""
    try:
        time.sleep(RATE_LIMIT_DELAY)
        response = llm.invoke(prompt)

        if not response.content:
            raise ValueError("Empty response from LLM")

        # Clean up the response text
        response_text = response.content.strip()
        
        # Try to find and extract the JSON part
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end != 0:
            try:
                json_str = response_text[start:end]
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                console.print(f"[yellow]Failed to parse JSON: {str(e)}[/yellow]")
        
        # Return empty structure if parsing fails
        return {
            "network_elements": [],
            "states": [],
            "transitions": [],
            "network_element_relationships": [],
            "triggers": [],
            "conditions": [],
            "timing": []
        }

    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            console.print(f"[yellow]API quota exceeded. Waiting before retry...[/yellow]")
            time.sleep(RATE_LIMIT_DELAY * 5)
            raise
        console.print(f"[red]Error calling LLM: {str(e)}[/red]")
        raise

def is_relevant_chunk(text: str) -> bool:
    """Enhanced chunk relevance check with trigger detection"""
    text_lower = text.lower()
    
    # Check standard keywords
    has_standard_keywords = any(keyword.lower() in text_lower for keyword in RELEVANT_KEYWORDS)
    
    # Look for potential trigger patterns
    trigger_patterns = [
        r"(?:when|if)\s+.*(?:occurs|happens)",
        r"triggered\s+by\s+.*",
        r"initiated\s+(?:when|if)\s+.*",
        r"starts?\s+(?:when|if)\s+.*",
        r"in\s+case\s+of\s+.*",
        r"due\s+to\s+.*"
    ]
    
    has_trigger_pattern = any(re.search(pattern, text_lower) for pattern in trigger_patterns)
    
    console.print(f"[blue]Checking chunk relevance:[/blue]")
    if has_standard_keywords:
        console.print("[green]✓ Found standard keywords[/green]")
    if has_trigger_pattern:
        console.print("[green]✓ Found potential trigger pattern[/green]")
        
    return has_standard_keywords or has_trigger_pattern

def extract_additional_triggers(text: str) -> List[str]:
    """Extract initial registration triggers from text."""
    found_triggers = []
    
    # Define trigger patterns for each category
    INITIAL_REGISTRATION_TRIGGERS = {
        "Power On": [
            r"power.*on",
            r"UE.*start",
            r"initial.*power",
            r"device.*start"
        ],
        "Enter 5G Coverage": [
            r"enter.*5G",
            r"5G.*coverage",
            r"move.*to.*5G",
            r"detect.*5G"
        ],
        "Change of PLMN": [
            r"change.*PLMN",
            r"new.*PLMN",
            r"different.*PLMN",
            r"PLMN.*selection"
        ],
        "Change in Subscription": [
            r"subscription.*change",
            r"USIM.*update",
            r"new.*subscription",
            r"modify.*subscription"
        ],
        "Registration Area Change": [
            r"area.*change",
            r"new.*area",
            r"different.*area",
            r"tracking.*area"
        ]
    }
    
    # Check each trigger category and its patterns
    for trigger_name, patterns in INITIAL_REGISTRATION_TRIGGERS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if trigger_name not in found_triggers:
                    found_triggers.append(trigger_name)
                    console.print(f"[green]✓ Found trigger: {trigger_name}[/green]")
                    break
    
    if not found_triggers:
        console.print("[yellow]No specific initial registration triggers found[/yellow]")
    
    return found_triggers

def verify_registration_trigger(trigger: str) -> bool:
    """Verify if a trigger is related to Initial Registration"""
    # Check if the trigger matches any known trigger category
    return any(
        trigger_name.lower() in trigger.lower() or
        any(re.search(pattern, trigger, re.IGNORECASE) 
            for pattern in patterns)
        for trigger_name, patterns in INITIAL_REGISTRATION_TRIGGERS.items()
    )

def save_results(results: List[Dict], output_file: str):
    """Save results to JSON file with better error handling."""
    try:
        # First, check if we have valid results
        if not results:
            console.print("[yellow]No results to save[/yellow]")
            return

        # Process results to ensure they can be serialized
        processed_results = []
        for result in results:
            if isinstance(result, dict):
                if "error" not in result:
                    try:
                        # Validate using Pydantic model
                        procedure = RegistrationProcedure(**result)
                        processed_results.append(procedure.model_dump())
                    except ValidationError as ve:
                        console.print(f"[yellow]Skipping invalid result: {str(ve)}[/yellow]")
                else:
                    console.print(f"[yellow]Skipping result with error: {result['error']}[/yellow]")
            elif hasattr(result, 'model_dump'):
                processed_results.append(result.model_dump())
            else:
                console.print(f"[yellow]Warning: Skipping invalid result of type {type(result)}[/yellow]")

        # Create output data structure
        output_data = ExtractionResult(
            procedures=processed_results,
            total_procedures=len(results),
            successful_extractions=len(processed_results)
        )

        # Debug info
        console.print(f"\n[blue]Saving {len(processed_results)} processed results to {output_file}[/blue]")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data.model_dump(), f, indent=2, ensure_ascii=False)
            
        # Verify file was saved correctly
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            console.print(f"[green]✓ Results saved successfully ({file_size} bytes)[/green]")
            
            # Show first few lines of saved file for debugging
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    first_lines = ''.join([next(f) for _ in range(10)])
                console.print("[blue]Preview of saved file:[/blue]")
                console.print(first_lines)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not read back file for verification: {str(e)}[/yellow]")
        else:
            console.print("[red]Error: File not created[/red]")

    except Exception as e:
        console.print(f"[red]Error saving results: {str(e)}[/red]")
        console.print(traceback.format_exc())
        
        # Try to save backup with error info
        try:
            backup_file = output_file.replace('.json', '_backup.json')
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'error': str(e),
                    'metadata': {
                        'timestamp': datetime.now().isoformat(),
                        'total_results': len(results),
                        'successful_results': len(processed_results)
                    },
                    'raw_results': results
                }, f, indent=2, ensure_ascii=False)
            console.print(f"[yellow]Saved backup to {backup_file}[/yellow]")
        except Exception as backup_error:
            console.print(f"[red]Failed to save backup: {str(backup_error)}[/red]")

def save_intermediate_results(results: List[ValidatedData], output_dir: str):
    """Save already validated results"""
    try:
        output_data = {
            "results": [
                {
                    "data": result.data.dict(),
                    "validated": result.is_validated,
                    "validation_timestamp": result.validation_timestamp.isoformat()
                }
                for result in results
                if result and result.is_validated
            ]
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"intermediate_results_{timestamp}.json")
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
            
        console.print(f"[green]✓ Saved validated results to {output_file}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error saving results: {str(e)}[/red]")

def main():
    try:
        # Ensure folders exist
        ensure_folders_exist()

        # Initialize LLM
        llm = initialize_llm()

        # Process the markdown file
        all_results = process_md_chunks(INPUT_MD_FILE, llm)

        # Save final results to JSON and MD file
        save_results(all_results, OUTPUT_FILE)
        console.print("[green]✓ Processing completed successfully[/green]")

        # After processing chunks
        for result in all_results:
            if result:
                console.print("\n[blue]Verifying extraction result:[/blue]")
                verify_extraction(result)

    except Exception as e:
        console.print(f"[red]Error in main process: {str(e)}[/red]")
        console.print(traceback.format_exc())

    finally:
        # Ensure completion marker is saved even if there's an error
        save_completion_marker()

if __name__ == "__main__":
    main()
