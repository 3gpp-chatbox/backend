import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Set, Optional
from dotenv import load_dotenv
from rich.console import Console
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential
import traceback
from pathlib import Path
from pipeline.semantic_chunking import SemanticChunker, save_semantic_chunks
from models import (
    NetworkElement, 
    PeriodicRegistrationData, 
    PeriodicRegistrationStep, 
    PeriodicRegistrationMetadata
)
from pydantic import ValidationError
from langchain_core.messages import HumanMessage, SystemMessage
# Initialize console for better output
console = Console()

# Load environment variables
load_dotenv(override=True)

# Configuration
INPUT_MD_FILE = os.path.join("processed_data", "semantic_TS_24.501.md")  # Use semantic_chunks.md instead of .txt
PROCESSED_DATA_FOLDER = os.path.join("processed_data")
CHUNK_SIZE = 4000
LLM_MODEL = "gemini-2.0-flash"
OUTPUT_FILE = str(Path(PROCESSED_DATA_FOLDER) / "periodic_registration_analysis.json")
OUTPUT_MD_FILE = str(Path(PROCESSED_DATA_FOLDER) / "periodic_registration_analysis.md")
INTERMEDIATE_BATCH_SIZE = 10
RATE_LIMIT_DELAY = 1
MAX_RETRIES = 3

RELEVANT_KEYWORDS = [
    "periodic registration",
    "registration update",
    "T3512",
    "timer expiry",
    "rat change",
    "tracking area",
    "nssai",
    "service area",
    "registration accept",
    "registration request",
    "5GMM-REGISTERED",
    
    # Additional trigger-related keywords
    "trigger",
    "initiated by",
    "caused by",
    "when",
    "if",
    "condition",
    "change",
    "update",
    "modification"
]

EXTRACTION_PROMPT = '''You are an expert in 5G NAS signaling procedures as defined in 3GPP TS 24.501. Your task is to extract the complete execution flow of the Periodic Registration Procedure for each trigger and return it as structured JSON data for visualization.

IMPORTANT: Each procedure flow MUST include these three mandatory messages in order:
1. Registration Request (UE → AMF)
2. Registration Accept (AMF → UE)
3. Registration Complete (UE → AMF)

Triggers for Periodic Registration Procedure:
1. T3512 Timer Expiry (UE-initiated periodic registration)
2. Change in RAT (Radio Access Technology)
3. Change in Tracking Area List (TA List) with Active PDU Session
4. Change in Network Slice Selection Assistance Information (NSSAI)
5. Change in Service Area

### **Extraction Requirements:**
1. **Complete Message Extraction:**  
   - Extract all NAS signaling messages exchanged between UE and AMF, not just the three mandatory ones.  
   - Include optional messages such as Identity Request/Response, Authentication Request/Response, and any failure messages.  

2. **Decision Points and Alternative Flows:**  
   - Identify and include failure scenarios (e.g., AMF rejects request, retransmission, fallback to another RAT).  
   - Indicate alternative flows based on network conditions (e.g., active PDU session vs. inactive PDU session).  

3. **JSON Structure and Formatting:**  
   - **Nodes** represent individual steps in the procedure (e.g., UE detects timer expiry, sends message, waits for response).  
   - **Edges** must explicitly define the transition between steps, including retry attempts if applicable.  
   - **Node IDs** must be structured as `"A1"`, `"A2"`, etc., maintaining logical sequencing.  
   - **Nodes must include state type (5GMM-REGISTERED, 5GMM-DEREGISTERED, 5GMM-CONNECTED, 5GMM-DISCONNECTED, 5GMM-IDLE)**

4. **Metadata Extraction:**  
   - Extract and include key parameters such as GUTI, TMSI, network slice information, and timer values.  
   - Identify whether authentication/security updates occur during the procedure.  

### **Expected JSON Format example:**
{
  "procedure": "Periodic Registration",
  "trigger": "T3512 Timer Expiry",
  "nodes": [
    { "id": "A1", "label": "UE detects timer expiry", "source": "UE", "target": "UE", "state_type": "5GMM-IDLE" },
    { "id": "A2", "label": "UE sends Registration Request", "messageType": "Registration Request", "source": "UE", "target": "AMF", "state_type": "5GMM-IDLE" },
    { "id": "A3", "label": "AMF processes request", "source": "AMF", "target": "AMF", "state_type": "5GMM-IDLE" },
    { "id": "A4", "label": "AMF decision point: Accept or Reject?", "source": "AMF", "target": "AMF", "type": "decision", "state_type": "5GMM-IDLE" },
    
    { "id": "A5", "label": "AMF sends Registration Accept", "messageType": "Registration Accept", "source": "AMF", "target": "UE" },
    { "id": "A6", "label": "UE sends Registration Complete", "messageType": "Registration Complete", "source": "UE", "target": "AMF" },
    { "id": "A7", "label": "UE updates registration timer", "source": "UE", "target": "UE" },

    { "id": "B1", "label": "AMF rejects registration", "messageType": "Registration Reject", "source": "AMF", "target": "UE", "type": "error" },
    { "id": "B2", "label": "UE retries Registration Request after T3512 expiry", "source": "UE", "target": "AMF" }
  ],
  "edges": [
    { "from": "A1", "to": "A2", "label": "Trigger detected" },
    { "from": "A2", "to": "A3", "label": "NAS message sent to AMF" },
    { "from": "A3", "to": "A4", "label": "AMF processes request" },
    
    { "from": "A4", "to": "A5", "label": "AMF accepts registration", "condition": "Success" },
    { "from": "A5", "to": "A6", "label": "UE acknowledges" },
    { "from": "A6", "to": "A7", "label": "Periodic registration complete" },

    { "from": "A4", "to": "B1", "label": "AMF rejects registration", "condition": "Failure" },
    { "from": "B1", "to": "B2", "label": "UE retries after T3512 expiry" }
  ],
  "metadata": {
    "procedureName": "Periodic Registration Update",
    "specReference": "3GPP TS 24.501",
    "protocol": "5G NAS",
    "timer": "T3512",
    "parameters": {
      "GUTI": "Extracted if present",
      "TMSI": "Extracted if present",
      "NSSAI": "Extracted if applicable",
      "SecurityContext": "Updated/Reused"
    }
  }
}
'''

class ValidatedData:
    def __init__(self, data: PeriodicRegistrationData):
        self.data = data
        self.validation_timestamp = datetime.now()
        self.is_validated = True

def initialize_llm():
    """Initialize LLM with error handling."""
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("Missing Google API key. Please check your .env file.")

        console.print(f"[blue]Using Google Gemini: {LLM_MODEL}[/blue]")
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=0,
            max_output_tokens=8192,
            top_p=0.95,
            top_k=40
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


def process_md_chunks(md_file_path: str, llm) -> List[Dict]:
    """Process semantic chunks from markdown file."""
    try:
        console.print(f"\n[blue]Starting extraction process...[/blue]")
        console.print(f"[blue]Reading from: {md_file_path}[/blue]")
        
        # Convert to Path object for better path handling
        file_path = Path(md_file_path).resolve()
        console.print(f"[blue]Resolved path: {file_path}[/blue]")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # Debug: Show file content
        console.print(f"\n[yellow]File size: {len(md_content)} characters[/yellow]")

        # Split chunks
        chunks = md_content.split("## Semantic Chunk")[1:]
        console.print(f"\n[blue]Found {len(chunks)} chunks[/blue]")

        results = []
        for chunk_index, chunk in enumerate(chunks):
            console.print(f"\n[blue]Processing chunk {chunk_index + 1}/{len(chunks)}[/blue]")
            doc = Document(page_content=chunk, metadata={
                "source": md_file_path,
                "chunk_index": chunk_index,
                "total_chunks": len(chunks)
            })
            
            # Check if chunk is relevant
            is_relevant = is_relevant_chunk(doc.page_content)
            if is_relevant:
                console.print("[green]✓ Chunk contains relevant keywords or trigger patterns[/green]")
                console.print("[green]Processing chunk...[/green]")
                chunk_result = process_chunk(doc, llm)
                if chunk_result:
                    results.append(chunk_result)
                    console.print("[green]Successfully extracted data from chunk[/green]")
            else:
                console.print("[yellow]Skipping irrelevant chunk[/yellow]")
                continue

        console.print(f"\n[blue]Extraction complete. Found {len(results)} relevant results[/blue]")
        return results

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return []

def validate_llm_output(data: dict) -> Optional[ValidatedData]:
    """Validate LLM output and clean data if needed"""
    try:
        # Define valid state types
        VALID_STATE_TYPES = {
            "5GMM-REGISTERED",
            "5GMM-DEREGISTERED",
            "5GMM-CONNECTED",
            "5GMM-DISCONNECTED",
            "5GMM-IDLE"
        }

        # Define valid periodic registration triggers
        VALID_TRIGGERS = {
            "T3512 Timer Expiry",
            "Change in RAT",
            "Change in Tracking Area List",
            "Change in Network Slice Selection Assistance Information",
            "Change in NSSAI",
            "Change in Service Area"
        }

        # Define valid message types that can appear in the procedure
        VALID_MESSAGE_TYPES = {
            # Required messages
            "Registration Request",
            "Registration Accept",
            "Registration Complete",
            # Optional messages
            "Authentication Request",
            "Authentication Response",
            "Security Mode Command",
            "Security Mode Complete",
            "Identity Request",
            "Identity Response",
            "DL NAS Transport",
            "UL NAS Transport",
            "Registration Reject",
            "Configuration Update Command",
            "Configuration Update Complete"
        }

        # Check existing nodes for required messages
        has_request = False
        has_accept = False
        has_complete = False
        existing_nodes = data.get("nodes", [])
        
        # First pass: check existing messages
        for node in existing_nodes:
            msg_type = node.get("messageType", "").lower()
            if "registration request" in msg_type:
                has_request = True
            elif "registration accept" in msg_type:
                has_accept = True
            elif "registration complete" in msg_type:
                has_complete = True

        # Initialize nodes if empty or missing required messages
        if not existing_nodes or not (has_request and has_accept and has_complete):
            if not existing_nodes:
                data["nodes"] = []
            
            # Add missing mandatory messages while preserving existing ones
            if not has_request:
                data["nodes"].insert(0, {
                    "id": "A1",
                    "label": "UE sends Registration Request",
                    "source": "UE",
                    "target": "AMF",
                    "messageType": "Registration Request",
                    "state_type": "5GMM-REGISTERED"  # Initial state for registration request
                })
            
            if not has_accept:
                insert_pos = len(data["nodes"])
                for i, node in enumerate(data["nodes"]):
                    if "registration complete" in node.get("messageType", "").lower():
                        insert_pos = i
                        break
                data["nodes"].insert(insert_pos, {
                    "id": f"A{insert_pos + 1}",
                    "label": "AMF sends Registration Accept",
                    "source": "AMF",
                    "target": "UE",
                    "messageType": "Registration Accept",
                    "state_type": "5GMM-REGISTERED"  # State during registration accept
                })
            
            if not has_complete:
                data["nodes"].append({
                    "id": f"A{len(data['nodes']) + 1}",
                    "label": "UE sends Registration Complete",
                    "source": "UE",
                    "target": "AMF",
                    "messageType": "Registration Complete",
                    "state_type": "5GMM-REGISTERED"  # Final state after registration complete
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

            # Validate and set state_type
            if "state_type" not in node or node["state_type"] not in VALID_STATE_TYPES:
                # Infer state type based on message type and context
                msg_type = node.get("messageType", "").lower()
                if "registration request" in msg_type:
                    node["state_type"] = "5GMM-REGISTERED"
                elif "registration accept" in msg_type:
                    node["state_type"] = "5GMM-REGISTERED"
                elif "registration complete" in msg_type:
                    node["state_type"] = "5GMM-REGISTERED"
                else:
                    # Default to REGISTERED state for periodic registration procedure
                    node["state_type"] = "5GMM-REGISTERED"

            # Set or validate message type
            if "messageType" not in node:
                # Try to infer message type from label
                label_lower = node["label"].lower()
                for msg_type in VALID_MESSAGE_TYPES:
                    if msg_type.lower() in label_lower:
                        node["messageType"] = msg_type
                        break
                if "messageType" not in node:
                    node["messageType"] = "NAS Message"
            elif node["messageType"] not in VALID_MESSAGE_TYPES:
                # Try to map to a valid message type
                msg_lower = node["messageType"].lower()
                for valid_type in VALID_MESSAGE_TYPES:
                    if valid_type.lower() in msg_lower:
                        node["messageType"] = valid_type
                        break

        # Regenerate edges to ensure proper flow
        data["edges"] = []
        for i in range(len(data["nodes"]) - 1):
            data["edges"].append({
                "from": data["nodes"][i]["id"],
                "to": data["nodes"][i + 1]["id"],
                "label": f"Step {i+1} to {i+2}",
                "condition": "Success"
            })

        # Validate trigger
        if not data.get("trigger") or data["trigger"] not in VALID_TRIGGERS:
            # Try to infer trigger from nodes
            for node in data["nodes"]:
                for trigger in VALID_TRIGGERS:
                    if trigger.lower() in node["label"].lower():
                        data["trigger"] = trigger
                        break
            if not data.get("trigger"):
                data["trigger"] = "T3512 Timer Expiry"  # Default trigger

        # Create metadata if not present
        if "metadata" not in data:
            data["metadata"] = {
                "procedureName": "Periodic Registration Update",
                "specReference": "3GPP TS 24.501",
                "protocol": "5G NAS",
                "timer": "T3512" if "T3512" in data["trigger"] else None
            }

        # Convert to PeriodicRegistrationData
        validated_data = PeriodicRegistrationData(
            trigger=data["trigger"],
            description=data.get("description", "Periodic Registration Update procedure"),
            nodes=data["nodes"],
            edges=data["edges"],
            metadata=PeriodicRegistrationMetadata(**data["metadata"]),
            network_elements=data["network_elements"],
            procedure_flow=[
                PeriodicRegistrationStep(
                    sequence_number=i+1,
                    source=node["source"],
                    target=node["target"],
                    message=node["label"],
                    description=node["label"],
                    message_type=node["messageType"],
                    parameters=[],
                    conditions=[],
                    outcome=""
                ) for i, node in enumerate(data["nodes"])
            ]
        )

        return ValidatedData(validated_data)

    except Exception as e:
        console.print(f"[red]Validation error: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return None

def verify_extraction(data: dict) -> bool:
    """Verify if all required nodes and edges are extracted for periodic registration"""
    
    # Valid state types
    VALID_STATE_TYPES = {
        "5GMM-REGISTERED",
        "5GMM-DEREGISTERED",
        "5GMM-CONNECTED",
        "5GMM-DISCONNECTED",
        "5GMM-IDLE"
    }
    
    # Expected network elements for periodic registration (only UE and AMF needed)
    required_elements = {"UE", "AMF"}
    
    # Expected key messages in periodic registration procedure
    required_messages = {
        "Registration Request",
        "Registration Accept",
        "Registration Complete"
    }
    
    # Valid triggers for periodic registration
    valid_triggers = {
        "T3512 Timer Expiry",
        "Change in RAT",
        "Change in Tracking Area List",
        "Change in NSSAI",
        "Change in Service Area"
    }
    
    # Check network elements
    extracted_elements = {ne["name"] for ne in data.get("network_elements", [])}
    missing_elements = required_elements - extracted_elements
    
    # Check procedure flow and nodes with more flexible message matching
    extracted_messages = set()
    missing_state_types = []
    invalid_state_types = []
    
    # Check nodes for state types and messages
    for node in data.get("nodes", []):
        # Check message types
        message = node.get("message", "").lower()
        if "registration request" in message:
            extracted_messages.add("Registration Request")
        elif "registration accept" in message:
            extracted_messages.add("Registration Accept")
        elif "registration complete" in message:
            extracted_messages.add("Registration Complete")
            
        # Check state types
        state_type = node.get("state_type")
        if not state_type:
            missing_state_types.append(node.get("id", "unknown"))
        elif state_type not in VALID_STATE_TYPES:
            invalid_state_types.append(f"{node.get('id', 'unknown')}: {state_type}")
    
    missing_messages = required_messages - extracted_messages
    
    # Verify nodes and edges exist
    has_nodes = len(data.get("nodes", [])) > 0
    has_edges = len(data.get("edges", [])) > 0
    
    # Print verification results
    console.print("\n[blue]Periodic Registration Verification Results:[/blue]")
    
    # Check state types
    if missing_state_types:
        console.print(f"[red]Missing state types in nodes: {', '.join(missing_state_types)}[/red]")
    if invalid_state_types:
        console.print(f"[red]Invalid state types found: {', '.join(invalid_state_types)}[/red]")
    if not missing_state_types and not invalid_state_types:
        console.print("[green]✓ All nodes have valid state types[/green]")
    
    # Check trigger
    trigger = data.get("trigger")
    if trigger and trigger in valid_triggers:
        console.print(f"[green]✓ Valid trigger defined: {trigger}[/green]")
        has_valid_trigger = True
    else:
        console.print(f"[red]Invalid or missing trigger: {trigger}[/red]")
        console.print("[yellow]Valid triggers are:[/yellow]")
        for t in valid_triggers:
            console.print(f"[yellow]- {t}[/yellow]")
        has_valid_trigger = False
    
    # Check metadata
    metadata = data.get("metadata", {})
    if metadata:
        console.print(f"[green]✓ Spec Reference: {metadata.get('specReference')}[/green]")
        if metadata.get('timer'):
            console.print(f"[green]✓ Timer: {metadata['timer']}[/green]")
    
    # Check network elements
    if missing_elements:
        console.print(f"[red]Missing required network elements: {', '.join(missing_elements)}[/red]")
    else:
        console.print(f"[green]✓ All required network elements found: {', '.join(extracted_elements)}[/green]")
        
    # Check messages
    if missing_messages:
        console.print(f"[red]Missing required messages: {', '.join(missing_messages)}[/red]")
    else:
        console.print(f"[green]✓ All required messages found[/green]")
        
    # Check graph structure
    if not has_nodes:
        console.print("[red]Missing nodes in graph structure[/red]")
    if not has_edges:
        console.print("[red]Missing edges in graph structure[/red]")
        
    # Verify sequence
    if data.get("procedure_flow"):
        console.print("\n[blue]Message Sequence:[/blue]")
        for step in sorted(data["procedure_flow"], key=lambda x: x["sequence_number"]):
            message_info = f"{step['sequence_number']}. {step['source']} -> {step['target']}: {step['message']}"
            if step.get("message_type"):
                message_info += f" (Type: {step['message_type']})"
            if step.get("parameters"):
                message_info += f" [Parameters: {', '.join(step['parameters'])}]"
            console.print(f"[green]{message_info}[/green]")
    
    # Return overall verification result
    is_valid = (not missing_elements and 
                not missing_messages and 
                has_nodes and 
                has_edges and 
                has_valid_trigger and 
                not missing_state_types and 
                not invalid_state_types and 
                metadata is not None)
    
    if is_valid:
        console.print("\n[green]✓ Periodic Registration extraction verified successfully[/green]")
    else:
        console.print("\n[red]Periodic Registration extraction verification failed[/red]")
    
    return is_valid

def verify_complete_response(data: dict) -> bool:
    """Verify if response contains all required elements for periodic registration"""
    
    # Check basic structure
    required_keys = {"trigger", "network_elements", "procedure_flow"}
    if not all(key in data for key in required_keys):
        console.print("[red]Missing required sections in response[/red]")
        return False
        
    # Check network elements (only UE and AMF required for periodic registration)
    required_elements = {"UE", "AMF"}
    found_elements = {ne["name"] for ne in data.get("network_elements", [])}
    if not required_elements.issubset(found_elements):
        console.print(f"[red]Missing network elements: {required_elements - found_elements}[/red]")
        return False
        
    # Check procedure flow (only registration messages required)
    required_messages = {
        "Registration Request",
        "Registration Accept",
        "Registration Complete"
    }
    found_messages = {step["message"] for step in data.get("procedure_flow", [])}
    if not required_messages.issubset(found_messages):
        console.print(f"[red]Missing messages: {required_messages - found_messages}[/red]")
        return False
        
    # Check if procedure flow has correct sequence numbers
    flow_steps = data.get("procedure_flow", [])
    if not flow_steps or len(flow_steps) < 3:  # Minimum 3 steps for periodic registration
        console.print("[red]Incomplete procedure flow[/red]")
        return False
        
    # Check if conditions are present and non-empty
    for step in flow_steps:
        if not step.get("conditions"):
            console.print(f"[yellow]Warning: Missing conditions for step {step['sequence_number']}: {step['message']}[/yellow]")
            # Add default conditions based on message type
            if "Registration Request" in step["message"]:
                step["conditions"] = ["Timer expired or trigger condition met"]
            elif "Registration Accept" in step["message"]:
                step["conditions"] = ["UE authenticated", "Registration request valid"]
            elif "Registration Complete" in step["message"]:
                step["conditions"] = ["Registration Accept received"]
            else:
                step["conditions"] = ["Prerequisite steps completed"]
    
    # All checks passed
    console.print("[green]✓ Response verification complete - all elements present[/green]")
    return True

def process_chunk(doc: Document, llm: Any) -> List[Dict]:
    try:
        chunk_info = f"Processing chunk {doc.metadata['chunk_index'] + 1}/{doc.metadata['total_chunks']}"
        console.print(f"\n[blue]{chunk_info}[/blue]")
        
        if not is_relevant_chunk(doc.page_content):
            console.print("[yellow]Skipping irrelevant chunk[/yellow]")
            return []
            
        console.print("[green]Processing relevant chunk...[/green]")
        
        messages = [
            SystemMessage(content=EXTRACTION_PROMPT),
            HumanMessage(content=f"Extract ALL periodic registration triggers and their flows from this text:\n\n{doc.page_content}")
        ]
        
        try:
            # Call LLM
            response = llm.invoke(messages)
            response_text = response.content.strip()
            
            # Debug: Show raw LLM response
            console.print("\n[blue]Raw LLM Response:[/blue]")
            console.print(response_text)
            
            # Find JSON array in response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start >= 0 and json_end > 0:
                json_str = response_text[json_start:json_end]
                console.print("\n[blue]Attempting to parse JSON array[/blue]")
                
                try:
                    # Remove any markdown formatting
                    json_str = re.sub(r'```json\s*|\s*```', '', json_str)
                    json_str = json_str.strip()
                    
                    # Parse the JSON array
                    data_list = json.loads(json_str)
                    if not isinstance(data_list, list):
                        data_list = [data_list]
                    
                    # Debug: Show parsed structure
                    console.print("\n[blue]Parsed Data Structure:[/blue]")
                    for data in data_list:
                        console.print(json.dumps(data, indent=2))
                    
                    results = []
                    for data in data_list:
                        # Ensure required network elements
                        if "network_elements" not in data:
                            data["network_elements"] = [
                                {
                                    "name": "UE",
                                    "type": "Network Element",
                                    "description": "User Equipment initiating periodic registration"
                                },
                                {
                                    "name": "AMF",
                                    "type": "Network Element",
                                    "description": "Access and Mobility Management Function handling registration"
                                }
                            ]
                        
                        # Validate the extracted data
                        validated_data = validate_llm_output(data)
                        if validated_data and verify_extraction(validated_data.data.model_dump()):
                            console.print(f"[green]✓ Successfully validated data for trigger: {data.get('trigger', 'unknown')}[/green]")
                            results.append(validated_data.data.model_dump())
                        else:
                            console.print(f"[yellow]Failed to validate data for trigger: {data.get('trigger', 'unknown')}[/yellow]")
                    
                    return results
                except json.JSONDecodeError as e:
                    console.print(f"[red]JSON Parse Error: {str(e)}[/red]")
                    console.print(f"[yellow]Attempted to parse:[/yellow]\n{json_str[:1000]}...")
                    return []
            else:
                console.print("[red]No JSON array structure found in response[/red]")
                return []
                
        except Exception as e:
            console.print(f"[red]Error calling LLM: {str(e)}[/red]")
            console.print(traceback.format_exc())
            return []

    except Exception as e:
        console.print(f"[red]Error processing chunk: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return []

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

def save_results(results: List[Dict], output_file: str):
    """Save results to JSON file with better error handling."""
    try:
        # First, check if we have valid results
        if not results:
            console.print("[yellow]No results to save[/yellow]")
            return

        # Even if validation fails, we'll save the raw results
        output_data = {
            'metadata': {
                'extraction_time': datetime.now().isoformat(),
                'total_documents': len(results)
            },
            'results': results  # Save raw results directly
        }

        # Debug info
        console.print(f"\n[blue]Saving {len(results)} results to {output_file}[/blue]")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        # Verify file was saved correctly
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            console.print(f"[green]✓ Results saved successfully ({file_size} bytes)[/green]")
        else:
            console.print("[red]Error: File not created[/red]")

    except Exception as e:
        console.print(f"[red]Error saving results: {str(e)}[/red]")
        console.print(traceback.format_exc())

def extract_additional_triggers(text: str) -> List[str]:
    """Extract periodic registration triggers from text."""
    periodic_triggers = {
        "T3512 Timer Expiry": [
            r"T3512.*expir",
            r"timer.*T3512",
            r"periodic.*timer"
        ],
        "Change in RAT": [
            r"change.*RAT",
            r"RAT.*change",
            r"Radio Access Technology.*change",
            r"different.*RAT"
        ],
        "Change in Tracking Area List": [
            r"change.*TA List",
            r"Tracking Area.*change",
            r"new.*Tracking Area",
            r"different.*TA"
        ],
        "Change in NSSAI": [
            r"change.*NSSAI",
            r"NSSAI.*change",
            r"Network Slice.*change",
            r"new.*NSSAI"
        ],
        "Change in Service Area": [
            r"change.*Service Area",
            r"Service Area.*change",
            r"new.*Service Area",
            r"different.*Service Area"
        ]
    }
    
    found_triggers = []
    
    for trigger_name, patterns in periodic_triggers.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                if trigger_name not in found_triggers:
                    found_triggers.append(trigger_name)
                    console.print(f"[green]✓ Found trigger: {trigger_name}[/green]")
                break
    
    if not found_triggers:
        console.print("[yellow]No specific periodic registration triggers found[/yellow]")
    
    return found_triggers

def verify_registration_trigger(trigger: str) -> bool:
    """Verify if a trigger is related to Periodic Registration"""
    valid_triggers = {
        "T3512 Timer Expiry",
        "Change in RAT",
        "Change in Tracking Area List",
        "Change in NSSAI",
        "Change in Service Area"
    }
    
    # Direct match with valid triggers
    if trigger in valid_triggers:
        return True
    
    # Check for keyword matches
    trigger_lower = trigger.lower()
    trigger_indicators = [
        "periodic registration",
        "registration update",
        "t3512",
        "timer expiry",
        "rat change",
        "tracking area",
        "nssai",
        "service area"
    ]
    
    return any(indicator in trigger_lower for indicator in trigger_indicators)

def main():
    try:
        # Ensure folders exist
        ensure_folders_exist()

        # Initialize LLM
        llm = initialize_llm()

        # Process the markdown file
        chunk_results = process_md_chunks(INPUT_MD_FILE, llm)
        
        # Debug: Show chunk results
        console.print(f"\n[blue]Initial chunk results count: {len(chunk_results)}[/blue]")
        
        # Flatten results if needed (since each chunk can now return multiple results)
        all_results = []
        for chunk_result in chunk_results:
            if isinstance(chunk_result, list):
                all_results.extend(chunk_result)
            else:
                all_results.append(chunk_result)

        # Debug: Show flattened results
        console.print(f"\n[blue]Flattened results count: {len(all_results)}[/blue]")
        if all_results:
            console.print("\n[blue]First result structure:[/blue]")
            console.print(json.dumps(all_results[0], indent=2)[:1000] + "...")

        # Save final results to JSON file only
        save_results(all_results, OUTPUT_FILE)
        console.print("[green]✓ Processing completed successfully[/green]")

        # After processing chunks
        console.print(f"\n[blue]Found {len(all_results)} total triggers across all chunks[/blue]")
        for result in all_results:
            if result:
                console.print(f"\n[blue]Verifying extraction result for trigger: {result.get('trigger', 'unknown')}[/blue]")
                verify_extraction(result)

    except Exception as e:
        console.print(f"[red]Error in main process: {str(e)}[/red]")
        console.print(traceback.format_exc())

if __name__ == "__main__":
    main()
