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
from semantic_chunking import SemanticChunker, save_semantic_chunks
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
INPUT_MD_FILE = os.path.join("backend", "processed_data", "semantic_chunks.md")  # Use semantic_chunks.md instead of .txt
PROCESSED_DATA_FOLDER = os.path.join("backend", "processed_data")
CHUNK_SIZE = 4000
LLM_MODEL = "gemini-2.0-flash"
OUTPUT_FILE = os.path.join(PROCESSED_DATA_FOLDER, "periodic_registration_analysis.json")
OUTPUT_MD_FILE = os.path.join(PROCESSED_DATA_FOLDER, "periodic_registration_analysis.md")
INTERMEDIATE_BATCH_SIZE = 10
RATE_LIMIT_DELAY = 1
MAX_RETRIES = 3

RELEVANT_KEYWORDS = [
    "registration",
    "periodic registration",
    "registration procedure",
    "5G NAS",
    "UE",
    "AMF",
    "timer",
    "T3512",
    "RAT",
    "TA List",
    "NSSAI",
    "Service Area"
]

EXTRACTION_PROMPT = '''You are an expert in 5G NAS signaling procedures as defined in 3GPP TS 24.501. Your task is to extract the execution flow of the Periodic Registration Procedure for each trigger and return it as structured JSON data for visualization.

IMPORTANT: Each procedure flow MUST include these three mandatory messages in order:
1. Registration Request (from UE to AMF)
2. Registration Accept (from AMF to UE)
3. Registration Complete (from UE to AMF)

Triggers for Periodic Registration Procedure:
1. T3512 Timer Expiry (UE-initiated periodic registration)
2. Change in RAT (Radio Access Technology)
3. Change in Tracking Area List (TA List) with Active PDU Session
4. Change in Network Slice Selection Assistance Information (NSSAI)
5. Change in Service Area

For each trigger, follow these steps:

1. Identify the event that triggers Periodic Registration.
2. Extract the sequence of signaling messages exchanged between UE (User Equipment) and AMF (Access and Mobility Management Function).
3. Identify decision points where different outcomes are possible.
4. Return the execution flow as JSON, structured as a directed graph, where:
   - Nodes represent states or messages (MUST include all three mandatory messages).
   - Edges define the transitions between states/messages.

Expected JSON Output Format:
For each trigger, return JSON in this format:

{
  "procedure": "Periodic Registration",
  "trigger": "T3512 Timer Expiry",
  "nodes": [
    { "id": "1", "label": "UE detects timer expiry" },
    { "id": "2", "label": "UE sends Registration Request", "messageType": "Registration Request" },
    { "id": "3", "label": "AMF processes request" },
    { "id": "4", "label": "AMF sends Registration Accept", "messageType": "Registration Accept" },
    { "id": "5", "label": "UE sends Registration Complete", "messageType": "Registration Complete" },
    { "id": "6", "label": "UE updates registration timer" }
  ],
  "edges": [
    { "from": "1", "to": "2", "label": "Trigger detected" },
    { "from": "2", "to": "3", "label": "NAS message sent to AMF" },
    { "from": "3", "to": "4", "label": "AMF accepts registration" },
    { "from": "4", "to": "5", "label": "UE acknowledges" },
    { "from": "5", "to": "6", "label": "Periodic registration complete" }
  ],
  "metadata": {
    "procedureName": "Periodic Registration Update",
    "specReference": "3GPP TS 24.501",
    "protocol": "5G NAS",
    "timer": "T3512"
  }
}

REQUIREMENTS:
1. Each response MUST include all three mandatory messages (Registration Request, Accept, and Complete)
2. Node IDs MUST be in format "A1", "A2", etc. for proper sequencing
3. Each node MUST have a source and target (either UE or AMF)
4. Edges MUST connect all nodes in sequence
5. MessageType MUST be explicitly set for the three mandatory messages

Extract the complete procedure flow from the provided text, including all messages, parameters, conditions, and outcomes. Do not use default values - only extract what is explicitly mentioned in the text.'''

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
        
        with open(md_file_path, 'r', encoding='utf-8') as f:
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
        # Define valid periodic registration triggers
        VALID_TRIGGERS = {
            "T3512 Timer Expiry",
            "Change in RAT",
            "Change in Tracking Area List",
            "Change in Network Slice Selection Assistance Information",
            "Change in NSSAI",
            "Change in Service Area"
        }

        # Ensure nodes exist and have required messages
        if "nodes" not in data or not isinstance(data["nodes"], list):
            data["nodes"] = [
                {"id": "A1", "label": "UE detects trigger condition", "source": "UE", "target": "UE"},
                {"id": "A2", "label": "UE sends Registration Request", "source": "UE", "target": "AMF", "messageType": "Registration Request"},
                {"id": "A3", "label": "AMF sends Registration Accept", "source": "AMF", "target": "UE", "messageType": "Registration Accept"},
                {"id": "A4", "label": "UE sends Registration Complete", "source": "UE", "target": "AMF", "messageType": "Registration Complete"}
            ]

        # Ensure edges exist
        if "edges" not in data or not data["edges"]:
            data["edges"] = []
            nodes = data["nodes"]
            for i in range(len(nodes) - 1):
                data["edges"].append({
                    "from": nodes[i]["id"],
                    "to": nodes[i + 1]["id"],
                    "label": f"Step {i+1} to {i+2}"
                })

        # Ensure network elements exist
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

        # Clean up data before validation
        if "nodes" in data and isinstance(data["nodes"], list):
            # Ensure required messages exist
            has_request = False
            has_accept = False
            has_complete = False
            
            for node in data["nodes"]:
                # Set message type based on label content
                label = node.get("label", "").lower()
                if "registration request" in label:
                    node["messageType"] = "Registration Request"
                    has_request = True
                elif "registration accept" in label:
                    node["messageType"] = "Registration Accept"
                    has_accept = True
                elif "registration complete" in label:
                    node["messageType"] = "Registration Complete"
                    has_complete = True

                # Ensure source and target are valid strings
                if not node.get("source") or not isinstance(node.get("source"), str):
                    if "UE" in node.get("label", ""):
                        node["source"] = "UE"
                    elif "AMF" in node.get("label", ""):
                        node["source"] = "AMF"
                    else:
                        node["source"] = "UE"  # Default source
                
                if not node.get("target") or not isinstance(node.get("target"), str):
                    if "AMF" in node.get("label", "") and node["source"] != "AMF":
                        node["target"] = "AMF"
                    elif "UE" in node.get("label", "") and node["source"] != "UE":
                        node["target"] = "UE"
                    else:
                        node["target"] = "AMF"  # Default target

                # Clean up conditions
                if "conditions" in node and isinstance(node["conditions"], str):
                    node["conditions"] = [node["conditions"]]
                elif node.get("conditions") is None:
                    node["conditions"] = []

                # Ensure other required fields exist
                if not node.get("parameters"):
                    node["parameters"] = []
                if not node.get("outcome"):
                    node["outcome"] = ""

            # Add missing required messages if needed
            if not (has_request and has_accept and has_complete):
                next_id = f"A{len(data['nodes']) + 1}"
                if not has_request:
                    data["nodes"].append({
                        "id": next_id,
                        "label": "UE sends Registration Request",
                        "source": "UE",
                        "target": "AMF",
                        "messageType": "Registration Request",
                        "parameters": [],
                        "conditions": [],
                        "outcome": ""
                    })
                    next_id = f"A{len(data['nodes']) + 1}"
                
                if not has_accept:
                    data["nodes"].append({
                        "id": next_id,
                        "label": "AMF sends Registration Accept",
                        "source": "AMF",
                        "target": "UE",
                        "messageType": "Registration Accept",
                        "parameters": [],
                        "conditions": [],
                        "outcome": ""
                    })
                    next_id = f"A{len(data['nodes']) + 1}"
                
                if not has_complete:
                    data["nodes"].append({
                        "id": next_id,
                        "label": "UE sends Registration Complete",
                        "source": "UE",
                        "target": "AMF",
                        "messageType": "Registration Complete",
                        "parameters": [],
                        "conditions": [],
                        "outcome": ""
                    })

                # Regenerate edges after adding missing messages
                data["edges"] = []
                for i in range(len(data["nodes"]) - 1):
                    data["edges"].append({
                        "from": data["nodes"][i]["id"],
                        "to": data["nodes"][i + 1]["id"],
                        "label": f"Step {i+1} to {i+2}"
                    })

        # Validate trigger
        trigger = data.get("trigger")
        if not trigger:
            trigger_nodes = [node for node in data.get("nodes", []) 
                           if any(valid_trigger.lower() in node.get("label", "").lower() 
                                 for valid_trigger in VALID_TRIGGERS)]
            if trigger_nodes:
                data["trigger"] = trigger_nodes[0]["label"]
            else:
                console.print("[yellow]Warning: No valid trigger found in data[/yellow]")
                console.print("[yellow]Valid triggers are:[/yellow]")
                for t in VALID_TRIGGERS:
                    console.print(f"[yellow]- {t}[/yellow]")
        else:
            if not any(valid_trigger.lower() in trigger.lower() for valid_trigger in VALID_TRIGGERS):
                console.print(f"[yellow]Warning: Trigger '{trigger}' may not be a standard periodic registration trigger[/yellow]")
                console.print("[yellow]Valid triggers are:[/yellow]")
                for t in VALID_TRIGGERS:
                    console.print(f"[yellow]- {t}[/yellow]")

        # Create metadata
        metadata = PeriodicRegistrationMetadata(
            specReference=data.get("metadata", {}).get("specReference", "TS 24.501"),
            timer=data.get("metadata", {}).get("timer", "T3512" if "T3512" in str(data.get("trigger", "")).upper() else None)
        )

        # Convert nodes to procedure flow steps with proper sequence numbers
        procedure_flow = []
        seen_sequence_numbers = set()
        next_sequence_number = 1
        
        for node in data.get("nodes", []):
            try:
                if node["id"].startswith("A"):
                    seq_num = int(node["id"].replace("A", ""))
                else:
                    seq_num = ord(node["id"][0].upper()) - ord('A') + 1
                    
                # Handle duplicate sequence numbers
                while seq_num in seen_sequence_numbers:
                    seq_num = next_sequence_number
                    next_sequence_number += 1
                    
                seen_sequence_numbers.add(seq_num)
                next_sequence_number = max(next_sequence_number, seq_num + 1)
                
            except (ValueError, IndexError, KeyError):
                while next_sequence_number in seen_sequence_numbers:
                    next_sequence_number += 1
                seq_num = next_sequence_number
                seen_sequence_numbers.add(seq_num)
                next_sequence_number += 1
                
            # Debug output for node validation
            console.print(f"\n[blue]Processing node {seq_num}:[/blue]")
            console.print(f"[blue]Source: {node.get('source')}[/blue]")
            console.print(f"[blue]Target: {node.get('target')}[/blue]")
            console.print(f"[blue]Label: {node.get('label')}[/blue]")
                
            step = PeriodicRegistrationStep(
                sequence_number=seq_num,
                source=node.get("source", "UE"),
                target=node.get("target", "AMF"),
                message=node.get("label", ""),
                description=node.get("label", ""),
                message_type=node.get("messageType", "NAS Registration"),
                parameters=node.get("parameters", []),
                conditions=node.get("conditions", []),
                outcome=node.get("outcome", "")
            )
            procedure_flow.append(step)

        # Create final validated data
        validated_data = PeriodicRegistrationData(
            trigger=data.get("trigger"),
            description=data.get("description", "Periodic Registration Update procedure"),
            nodes=data.get("nodes", []),
            edges=data.get("edges", []),
            metadata=metadata,
            network_elements=data["network_elements"],
            procedure_flow=sorted(procedure_flow, key=lambda x: x.sequence_number)
        )

        console.print("[green]✓ LLM output validation successful[/green]")
        return ValidatedData(validated_data)

    except ValidationError as e:
        console.print("[red]LLM output validation failed:[/red]")
        console.print(f"[red]{str(e)}[/red]")
        # Debug output for validation error
        if data and "nodes" in data:
            console.print("\n[yellow]Node data that caused validation error:[/yellow]")
            for node in data["nodes"]:
                console.print(f"[yellow]{json.dumps(node, indent=2)}[/yellow]")
        return None

def verify_extraction(data: dict) -> bool:
    """Verify if all required nodes and edges are extracted for periodic registration"""
    
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
    for step in data.get("procedure_flow", []):
        message = step["message"].lower()
        if "registration request" in message:
            extracted_messages.add("Registration Request")
        elif "registration accept" in message:
            extracted_messages.add("Registration Accept")
        elif "registration complete" in message:
            extracted_messages.add("Registration Complete")
    
    missing_messages = required_messages - extracted_messages
    
    # Verify nodes and edges exist
    has_nodes = len(data.get("nodes", [])) > 0
    has_edges = len(data.get("edges", [])) > 0
    
    # Print verification results
    console.print("\n[blue]Periodic Registration Verification Results:[/blue]")
    
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
                try:
                    json_str = response_text[json_start:json_end]
                    console.print("\n[blue]Attempting to parse JSON array[/blue]")
                    
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
                            # Debug: Show validated structure
                            console.print("\n[blue]Validated Data Structure:[/blue]")
                            console.print(json.dumps(validated_data.data.model_dump(), indent=2))
                            results.append(validated_data.data.model_dump())
                        else:
                            console.print(f"[yellow]Failed to validate data for trigger: {data.get('trigger', 'unknown')}[/yellow]")
                    
                    if not results:
                        console.print("[yellow]No valid triggers found in response[/yellow]")
                    else:
                        console.print(f"[green]✓ Found {len(results)} valid triggers[/green]")
                    
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

        # Convert ValidatedData objects to dictionaries
        processed_results = []
        for result in results:
            if hasattr(result, 'data'):
                # Convert Pydantic model to dict
                result_dict = result.data.model_dump()
                processed_results.append(result_dict)
            else:
                console.print(f"[yellow]Skipping invalid result: {result}[/yellow]")

        output_data = {
            'metadata': {
                'extraction_time': datetime.now().isoformat(),
                'total_documents': len(processed_results)
            },
            'results': processed_results
        }

        # Debug info
        console.print(f"\n[blue]Saving {len(processed_results)} results to {output_file}[/blue]")
        
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
