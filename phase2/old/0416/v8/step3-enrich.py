import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

load_dotenv()

flash_model = "gemini-2.0-flash"
pro_model = "gemini-2.0-pro-exp-02-05"
new_model = "gemini-2.5-pro-exp-03-25"

# Load the Google API Key from the .env file
load_dotenv(override=True)


# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. Please set it in your .env file."
    )

client = genai.Client(api_key=api_key)


class Node(BaseModel):
    """Represents a State or Event in the process"""
    id: str = Field(..., description="Unique identifier for the node (e.g., number, 'start', 'end').")
    type: Literal["state", "event"] = Field(..., description="Type of the node, either 'state' or 'event'.")
    description: str = Field(..., description="Brief explanation of the state or event.")

class Edge(BaseModel):
    """Represents a Trigger or Condition connecting Nodes"""
    from_node: str = Field(..., alias="from", description="ID of the starting node.")
    to: str = Field(..., description="ID of the target node.")
    type: str = Field(..., description="Type of the edge, either 'trigger' or 'condition'.")
    description: str = Field(..., description="Explanation of the trigger or condition.")

class Graph(BaseModel):
    """Graph structure containing all States, Events, Triggers, and Conditions"""
    nodes: List[Node] = Field(..., description="List of all states and events.")
    edges: List[Edge] = Field(..., description="List of all triggers and conditions.")





def read_json_file(file_path):
    """Reads content from a JSON file and returns the parsed JSON object."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def read_text_file(file_path):
    """Reads content from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_procedural_info(section_name, extracted_data, original_content):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
You are a 3GPP procedure analysis expert. You are given **two parts of context** for the procedure: "{section_name}".

---

##  Provided Context

### 1. **First Part**:  
An extracted Flow Property Graph (FPG) for the procedure "{section_name}" on the UE side.  
- **Nodes** represent UE states.  
- **Edges** represent transitions between states, each with a basic structure.

### 2. **Second Part**:  
The **original 3GPP specification text** that defines this procedure in detail.

---

##  Your Task

Your job is to **enrich the flow property graph (FPG)** using the specification content — but **strictly without modifying** any existing structure.

###  What you must do:
- **DO NOT** delete or change any existing nodes or edges.
- **DO ONLY** add new information to enrich each `node` and `edge`.

###  What to Enrich:

#### For each `node` (state):
Add a `properties` field with optional metadata, if explicitly present:
- `"description"`: Short textual description of the state (if present in spec)
- `"cause_value"`: Optional
- `"timer_active"` or other relevant state indicators
- Any explicitly mentioned parameters (e.g., `"T3510"`, `"registration_attempt_counter"`)

#### For each `edge` (transition):
Add the following fields if they are **explicitly described**:
- `"event"`: The trigger that causes the state transition (e.g., message received, timer expired)
events should have properties (description, message type, timer trigger, etc.),parameters (values referenced by conditions or the event message)
- `"condition"`: List of all required conditions (logical checks, gating rules)
- `"action"`: List of UE actions taken (in response to the event/condition)
- `"properties"`: Add structured metadata if available:
  - `"parameters"`: Referenced variables (e.g., counters, timers)
  - `"context"`: Environmental or security context (e.g., `"security_context": "valid"`)
  - `"metadata"`: Any other optional descriptors like `"message_type"`
  - `"section_reference"`: The 3GPP spec section this transition comes from

---

##  Strict Rules

-  Use **only** the information from the provided graph and original 3GPP text.
-  **Do not infer** or assume anything that is not explicitly stated.
-  **Do not remove or alter** any part of the original extracted graph.
-  You may only **add** fields to enrich it.

---

##  Example Output Format

```json
{{
  "nodes": [
    {{
      "id": "node1",
      "name": "5GMM-REGISTERED",
      "properties": {{
        "description": "UE is successfully registered",
        "cause_value": "3GPP-defined cause",
        "timer_active": "T3502"
      }},
      "parameters": ["T3502"]
    }}
  ],
  "edges": [
    {{
      "id": "edge1",
      "from": "5GMM-REGISTERED",
      "to": "5GMM-DEREGISTERED",
      "event": [
      name:"Receive DEREGISTRATION REQUEST",
        "properties": {{
        "description": "receives deregistration request from network",
        "cause_value": "3GPP-defined cause",
         "section_reference": "5.5.1.2.1"
      }},
      "parameters": ["cause_value", "deregistration_type"]

      ]

      "condition": [
        "security_context = valid",
        "emergency_service_flag = false"
      ],
      "action": [
        "Stop T3502",
        "Send DEREGISTRATION ACCEPT"
      ],
      "properties": {{
        "parameters": ["security_context", "emergency_service_flag"],
        "context": {{
          "security_context": "valid"
        }},
        "metadata": {{
          "message_type": "DEREGISTRATION REQUEST"
        }},
        "section_reference": "5.5.1.2.3"
      }}
    }}
  ]
}}


First Part:
flow property graph the procedure "{section_name}" (Extracted previously):
{json.dumps(extracted_data, indent=2)}

------------------
Second Part:
Original Content from the 3GPP Specification:
{original_content}


  """


    model_to_use = new_model  # or pro_model depending on your requirement
    response = client.models.generate_content(
        model=model_to_use,
        contents=prompt,
        config={
            "temperature": 0,
             "response_mime_type": "application/json",
         

          
        },
    )

    # Extract the text content from the response
    procedural_info = response.text.strip() if hasattr(response, 'text') else str(response)

    return procedural_info

def save_to_json(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")



def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    extracted_data = read_json_file("v1-step3-correct.json")
    original_content = read_text_file("5.5.1.2.txt")

    if extracted_data is None or original_content is None:
        print("Failed to load extracted_data or original_content")
        return None

    procedural_info = extract_procedural_info(section_name, extracted_data, original_content)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "v1-step4-enrich.json")
else:
    print("Failed to extract")
