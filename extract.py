import os
import re
import json
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Any, Set, Optional
from dotenv import load_dotenv
from rich.console import Console
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential
import traceback
from pathlib import Path
import sys
import threading
import subprocess
from semantic_chunking import SemanticChunker, save_semantic_chun
from models import RegistrationAnalysis, NetworkElement, State, RegistrationStep, Metadata
from models import RegistrationData, NetworkElement, ProcedureStep, Procedure
from pydantic import ValidationError
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize console for better output
console = Console()

# Load environment variables
load_dotenv(override=True)

# Configuration
INPUT_MD_FILE = os.path.join("processed_data", "semantic_chunks.md")  # Use semantic_chunks.md instead of .txt
PROCESSED_DATA_FOLDER = os.path.join("processed_data")
CHUNK_SIZE = 4000
LLM_MODEL = "gemini-2.0-flash"
OUTPUT_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.json")
OUTPUT_MD_FILE = os.path.join(PROCESSED_DATA_FOLDER, "registration_analysis.md")
INTERMEDIATE_BATCH_SIZE = 10
RATE_LIMIT_DELAY = 1
MAX_RETRIES = 3


EXTRACTION_PROMPT = """Analyze the text and extract the 5G Initial Registration procedure flow.
You must include ALL required network elements and messages in your response.For each step, include ALL conditions that must be met.
>>>>>>> f6782aa2945b2d8857cc56efcdb82409178f0d5a

Example of conditions:
- For Registration Request: ["No current registration exists", "UE in 5GMM-DEREGISTERED state"]
- For Authentication: ["Security context not exists", "Authentication required"]
- For Security Mode: ["Authentication successful", "Security capabilities received"]


Required Network Elements (ALL must be included):
- UE (User Equipment)
- AMF (Access and Mobility Management Function)
- AUSF (Authentication Server Function)
- UDM (Unified Data Management)
- PCF (Policy Control Function)
- NSSF (Network Slice Selection Function)
- SMSF (SMS Forwarding Function)
- GGSF (Gateway GPRS Support Function)
- HSS (Home Subscriber Server)
- SMF (Session Management Function)


Required Messages (ALL must be included):
1. Registration Request (UE → AMF)
2. Authentication Request (AMF → UE)
3. Authentication Vector Request (AUSF → UDM)
4. Authentication Response (UE → AMF)
5. Security Mode Command (AMF → UE)
6. Security Mode Complete (UE → AMF)
7. Registration Accept (AMF → UE)
8. Registration Complete (UE → AMF)

Return ONLY this exact JSON structure with all required elements:

{
    "procedure": {
        "name": "Initial Registration",
        "description": "Complete 5G Initial Registration procedure"
    },
    "network_elements": [
        {
            "name": "UE",
            "type": "Network Element",
            "description": "User Equipment initiating registration"

        }
        // Include ALL network elements listed above
    ],
    "procedure_flow": [
        {
            "sequence_number": 1,
            "source": "UE",
            "target": "AMF",
            "message": "Registration Request",
            "description": "UE initiates registration procedure",
            "source_state": "5GMM-DEREGISTERED",
            "target_state": "5GMM-REGISTERED-INITIATED",
            "trigger": ["UE sends Registration Request to AMF", "UE power on", "UE out of coverage", "UE needs to establish an emergency PDU session","UE needs to establish an emergency PDU session"],
            "conditions": ["UE is not yet registered and has a valid PLMN"],  # Must be a list with [ ]
            "timing": "Start T3510"
            "response": "AMF sends Authentication Request to UE"
        }
        // Include ALL 8 messages listed above in correct sequence
    ]
}

Important: Your response must include ALL network elements and ALL messages listed above.The 'conditions' field must be a list (array) with square brackets [ ], even if empty: []

Text to analyze:
"""
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
        # Clean up data before validation
        if "procedure_flow" in data:
            for step in data["procedure_flow"]:
                # Convert trigger from list to string if needed
                if isinstance(step.get("trigger"), list):
                    step["trigger"] = " ".join(step["trigger"])
                
                # Ensure conditions is a list
                if "conditions" in step:
                    if isinstance(step["conditions"], str):
                        step["conditions"] = [step["conditions"]]
                    elif step["conditions"] is None:
                        step["conditions"] = []

        validated_data = RegistrationData(**data)
        console.print("[green]✓ LLM output validation successful[/green]")
        return ValidatedData(validated_data)
    except ValidationError as e:
        console.print("[red]LLM output validation failed:[/red]")
        console.print(f"[red]{str(e)}[/red]")
        return None

def verify_extraction(data: dict) -> bool:
    """Verify if all required nodes and edges are extracted"""
    
    # Expected network elements
    required_elements = {"UE", "AMF", "AUSF", "UDM", "SMF"}
    
    # Expected key messages in procedure
    required_messages = {
        "Registration Request",
        "Authentication Request",
        "Authentication Vector Request",
        "Authentication Response",
        "Security Mode Command",
        "Security Mode Complete",
        "Registration Accept",
        "Registration Complete"
    }
    
    # Check network elements
    extracted_elements = {ne["name"] for ne in data.get("network_elements", [])}
    missing_elements = required_elements - extracted_elements
    
    # Check procedure flow
    extracted_messages = {step["message"] for step in data.get("procedure_flow", [])}
    missing_messages = required_messages - extracted_messages
    
    # Print verification results
    console.print("\n[blue]Verification Results:[/blue]")
    
    if missing_elements:
        console.print(f"[red]Missing network elements: {', '.join(missing_elements)}[/red]")
    else:
        console.print(f"[green]✓ All required network elements found: {', '.join(extracted_elements)}[/green]")
        
    if missing_messages:
        console.print(f"[red]Missing messages: {', '.join(missing_messages)}[/red]")
    else:
        console.print(f"[green]✓ All required messages found[/green]")
        
    # Verify sequence
    steps = data.get("procedure_flow", [])
    if steps:
        console.print("\n[blue]Message Sequence:[/blue]")
        for step in sorted(steps, key=lambda x: x["sequence_number"]):
            console.print(f"[green]{step['sequence_number']}. {step['source']} -> {step['target']}: {step['message']}[/green]")
    
    return not (missing_elements or missing_messages)

def process_chunk(doc: Document, llm: Any) -> Dict:
    try:
        chunk_info = f"Processing chunk {doc.metadata['chunk_index'] + 1}/{doc.metadata['total_chunks']}"
        console.print(f"\n[blue]{chunk_info}[/blue]")
        
        if not is_relevant_chunk(doc.page_content):
            console.print("[yellow]Skipping irrelevant chunk[/yellow]")
            return None
            
        console.print("[green]Processing relevant chunk...[/green]")
        
        # Debug: Show chunk content
        console.print("\n[blue]Chunk content preview:[/blue]")
        console.print(doc.page_content[:200])
        
        messages = [
            SystemMessage(content="You are a 5G expert. Return ONLY a valid JSON object, nothing else."),
            HumanMessage(content=EXTRACTION_PROMPT + doc.page_content)
        ]
        
        # Extract and verify registration-specific triggers
        additional_triggers = extract_additional_triggers(doc.page_content)
        if additional_triggers:
            console.print("\n[blue]Found Initial Registration triggers:[/blue]")
            verified_triggers = []
            
            for trigger in additional_triggers:
                if verify_registration_trigger(trigger):
                    verified_triggers.append(trigger)
                    console.print(f"[green]✓ {trigger}[/green]")
                else:
                    console.print(f"[yellow]? {trigger} (not specific to Initial Registration)[/yellow]")
            
            # Use only verified triggers
            additional_triggers = verified_triggers
        
        # Add to LLM context if found
        if additional_triggers:
            context = "\nAdditional triggers found in text:\n" + "\n".join(f"- {t}" for t in additional_triggers)
            messages.append(HumanMessage(content=context))
        
        try:
            # Call LLM
            response = llm.invoke(messages)
            
            # Debug: Show raw response
            console.print("\n[blue]LLM Raw Response:[/blue]")
            console.print(response.content)
            
            # Clean response text
            response_text = response.content.strip()
            
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > 0:
                try:
                    json_str = response_text[json_start:json_end]
                    console.print("\n[blue]Extracted JSON:[/blue]")
                    console.print(json_str)
                    
                    data = json.loads(json_str)
                    if verify_complete_response(data):
                        validated_data = validate_llm_output(data)
                        if validated_data:
                            return validated_data
                except json.JSONDecodeError as e:
                    console.print(f"[red]JSON Parse Error: {str(e)}[/red]")
                    console.print(f"[yellow]Attempted to parse:[/yellow]\n{json_str[:200]}...")
            else:
                console.print("[red]No JSON structure found in response[/red]")
            
            return None
                
        except Exception as e:
            console.print(f"[red]Error calling LLM: {str(e)}[/red]")
            console.print(traceback.format_exc())
            return None
            
    except Exception as e:
        console.print(f"[red]Error processing chunk: {str(e)}[/red]")
        console.print(traceback.format_exc())
        return None

def verify_complete_response(data: dict) -> bool:
    """Verify if response contains all required elements including additional triggers"""
    
    # Check basic structure
    required_keys = {"procedure", "network_elements", "procedure_flow"}
    if not all(key in data for key in required_keys):
        console.print("[red]Missing required sections in response[/red]")
        return False
        
    # Check network elements (must have all 5)
    required_elements = {"UE", "AMF", "AUSF", "UDM", "SMF"}
    found_elements = {ne["name"] for ne in data.get("network_elements", [])}
    if not required_elements.issubset(found_elements):
        console.print(f"[red]Missing network elements: {required_elements - found_elements}[/red]")
        return False
        
    # Check procedure flow (must have all 8 messages)
    required_messages = {
        "Registration Request",
        "Authentication Request",
        "Authentication Vector Request",
        "Authentication Response",
        "Security Mode Command",
        "Security Mode Complete",
        "Registration Accept",
        "Registration Complete"
    }
    found_messages = {step["message"] for step in data.get("procedure_flow", [])}
    if not required_messages.issubset(found_messages):
        console.print(f"[red]Missing messages: {required_messages - found_messages}[/red]")
        return False
        
    # Check if procedure flow has correct sequence numbers
    flow_steps = data.get("procedure_flow", [])
    if not flow_steps or len(flow_steps) < 8:
        console.print("[red]Incomplete procedure flow[/red]")
        return False
        
    # Check if conditions are present and non-empty
    for step in flow_steps:
        if not step.get("conditions"):
            console.print(f"[yellow]Warning: Missing conditions for step {step['sequence_number']}: {step['message']}[/yellow]")
            # Add default conditions based on message type
            if "Registration Request" in step["message"]:
                step["conditions"] = ["No current registration exists", "UE in 5GMM-DEREGISTERED state"]
            elif "Authentication" in step["message"]:
                step["conditions"] = ["Security context not exists", "Authentication required"]
            elif "Security Mode" in step["message"]:
                step["conditions"] = ["Authentication successful", "Security capabilities received"]
            else:
                step["conditions"] = ["Prerequisite steps completed"]
    
    # All checks passed
    console.print("[green]✓ Response verification complete - all elements present[/green]")
    return True

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
    """Extract triggers specifically related to 5G Initial Registration"""
    triggers = []
    
    # Keywords specific to Initial Registration
    registration_keywords = [
        "initial registration", "5gmm-deregistered",
        "registration request", "registration accept",
        "authentication", "security mode", "registration complete"
    ]
    
    # Network elements involved in Initial Registration
    network_elements = [
        "UE", "AMF", "AUSF", "UDM", "SMF", "NSSF", 
        "PCF", "SMSF", "HSS", "GGSF"
    ]
    
    # Patterns for trigger extraction
    patterns = [
        r"(?:initial|new)\s+registration\s+(?:when|if)\s+(.*?)(?:[\.,]|$)",
        r"(?:UE|AMF)\s+initiates?\s+(?:initial)?\s*registration\s+(?:when|if)\s+(.*?)(?:[\.,]|$)",
        r"registration\s+(?:request|procedure)\s+is\s+triggered\s+(?:when|if)\s+(.*?)(?:[\.,]|$)"
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            trigger = match.group(1).strip()
            
            # Validate trigger
            is_valid = (
                any(kw.lower() in trigger.lower() for kw in registration_keywords) and
                any(ne.lower() in trigger.lower() for ne in network_elements) and
                len(trigger.split()) >= 3
            )
            
            if is_valid:
                trigger = trigger.strip('.,;: ')
                trigger = re.sub(r'\s+', ' ', trigger)
                if trigger not in triggers:
                    triggers.append(trigger)
                    console.print(f"[green]✓ Valid trigger: {trigger}[/green]")
    
    return triggers

def verify_registration_trigger(trigger: str) -> bool:
    """Verify if a trigger is related to Initial Registration"""
    registration_indicators = [
        "initial registration",
        "registration request",
        "first time registration",
        "new registration",
        "5gmm-deregistered",
        "registration procedure"
    ]
    
    return any(indicator.lower() in trigger.lower() for indicator in registration_indicators)

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

def save_results_to_md(results: List[Dict], output_file: str):
    """Save results to markdown file with better error handling."""
    try:
        if not results:
            console.print("[yellow]No results to save to markdown[/yellow]")
            return

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 5G Initial Registration Analysis\n\n")
            
            for result in results:
                if hasattr(result, 'data'):
                    data = result.data.model_dump()
                    
                    # Write procedure info
                    f.write(f"## {data['procedure']['name']}\n")
                    f.write(f"{data['procedure']['description']}\n\n")
                    
                    # Write network elements
                    f.write("### Network Elements\n")
                    for element in data['network_elements']:
                        f.write(f"- **{element['name']}**: {element['description']}\n")
                    f.write("\n")
                    
                    # Write procedure flow
                    f.write("### Procedure Flow\n")
                    for step in data['procedure_flow']:
                        f.write(f"\n#### {step['sequence_number']}. {step['message']}\n")
                        f.write(f"- **Source**: {step['source']}\n")
                        f.write(f"- **Target**: {step['target']}\n")
                        f.write(f"- **Description**: {step['description']}\n")
                        if step.get('source_state'):
                            f.write(f"- **Source State**: {step['source_state']}\n")
                        if step.get('target_state'):
                            f.write(f"- **Target State**: {step['target_state']}\n")
                        if step.get('trigger'):
                            f.write(f"- **Trigger**: {step['trigger']}\n")
                        if step.get('conditions'):
                            f.write("- **Conditions**:\n")
                            for condition in step['conditions']:
                                f.write(f"  - {condition}\n")
                        if step.get('timing'):
                            f.write(f"- **Timing**: {step['timing']}\n")
                    f.write("\n---\n\n")

        # Verify file was saved correctly
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            console.print(f"[green]✓ Markdown saved successfully ({file_size} bytes)[/green]")
        else:
            console.print("[red]Error: Markdown file not created[/red]")

    except Exception as e:
        console.print(f"[red]Error saving markdown: {str(e)}[/red]")
        console.print(traceback.format_exc())

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
        save_results_to_md(all_results, OUTPUT_MD_FILE)
        console.print("[green]✓ Processing completed successfully[/green]")

        # After processing chunks
        for result in all_results:
            if result:
                console.print("\n[blue]Verifying extraction result:[/blue]")
                verify_extraction(result.data.dict())

    except Exception as e:
        console.print(f"[red]Error in main process: {str(e)}[/red]")
        console.print(traceback.format_exc())

    finally:
        # Ensure completion marker is saved even if there's an error
        save_completion_marker()

if __name__ == "__main__":
    main()
