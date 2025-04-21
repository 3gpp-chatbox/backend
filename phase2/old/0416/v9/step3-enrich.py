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

## Provided Context
### 1. **Extracted Flow Property Graph (FPG)**  
This is a previously extracted graph for the procedure "{section_name}" on the **UE side only**.
- Nodes include:
  - **States**: Explicitly named UE states (e.g., "5GMM-REGISTERED", "DEREGISTERED.INITIAL").
  - **Events**: Triggers visible to the UE (e.g., "Receive DEREGISTRATION REQUEST", "T3510 expires").
- Edges represent directional transitions between these nodes:
  - From **State ➝ Event** (triggered by condition, entering event)
  - From **Event ➝ State** (resulting from action taken after event)
Each edge includes a simple label and the originating 3GPP section reference.

---

### 2. **Original 3GPP Specification Text**  
This is the raw spec text that describes the behavior and procedure details for the UE in section: "{section_name}".
---

##  Your Task: Enrich the Flow Property Graph

You must **only add new information** to enrich the graph using the original specification.  
 You are **not allowed to delete, rename, or modify** existing nodes or edges.
*"Ensure all enriched nodes/edges strictly represent UE behavior. Ignore network-side actions or conditions unless they directly trigger a UE state/event."*
---

###  Enrich the Nodes

#### For all `state` nodes:
Add a `properties` field with any **explicit** attributes found in the spec:
- `"description"`: brief summary
- `"cause_value"`: Only if stated
- `"timer_active"`: If a timer runs in this state
- Any mentioned parameters: e.g., `"T3510"`, `"registration_attempt_counter"`

#### For all `event` nodes:
Treat events as first-class elements (just like states). Add:
- `"description"`: What the event represents (e.g., “UE receives REGISTRATION ACCEPT”)
- `"parameters"`: List of referenced variables in this event (e.g., timers, causes, counters)
- `"properties"`:
  - `"message_type"`: If it's a message (e.g., “REGISTRATION REQUEST”)
  - `"timer_trigger"`: If it's caused by a timer
  - `"section_reference"`: Where this event is described

---

### Enrich the Edges

#### For each edge:
Add the following **only if explicitly found in the original spec**:

- `"condition"`: List of gating conditions required for this transition
- `"action"`: List of UE actions triggered by this transition (especially for Event ➝ State edges)
- `"properties"`:
  - `"parameters"`: Variables involved (e.g., `"T3510"`, `"emergency_service_flag"`)
  - `"context"`: Optional environmental details (e.g., `"security_context": "valid"`)
  - `"metadata"`: Any extra detail (e.g., `"message_type": "DEREGISTRATION REQUEST"`)
  - `"section_reference"`: Reference where this transition is defined

 Hint: Use the `from`/`to` direction and node `type` (state/event) to determine whether to enrich an edge with a condition or an action.
"For Event → State edges, include action for UE behaviors and condition only if the transition is explicitly gated (e.g., 'if X, UE enters STATE'). For State → Event edges, focus on conditions triggering the event."
Pay special attention to error handling clauses (e.g., 'if...else...') and ensure they are captured as conditions or actions.
---

##  Important Rules

- Only use information **explicitly described** in the original spec.*"Explicitly described" includes:
Direct quotes (e.g., "the UE shall start T3510").
Clear cause-and-effect (e.g., "upon reception of X, the UE enters Y").
Avoid inferring indirect actions (e.g., timer stops unless stated)."*

- Do **not infer** or assume anything outside the given content.
- Do **not rename, remove, or restructure** any nodes or edges.
- Only **add** to the existing graph.


Additional Rules for Clarity:

Network-Side Filtering: Ignore any network-side actions (e.g., "AMF sends...") unless they directly trigger a UE event.
Implicit vs. Explicit: *Capture timer starts, stops, resets, or modifications only if explicitly commanded (e.g., 'UE shall stop/reset/start T3510').*
Error Paths: Enrich edges with error-related conditions/actions (e.g., "if authentication fails, UE increments counter").
Multi-Section References: Aggregate all relevant spec sections for a node/edge if needed.
Message Parameters: For events like "Receive X", include parameters only if the spec lists them (e.g., "cause value #5" in a message).
---

##  Output Format Example

```json
{{
  "procedure_name": "{{section_name}}",
  "graph": {{
    "nodes": [
      {{
        "id": "node1",
        "name": "5GMM-DEREGISTERED",
        "type": "state",
        "description": "UE is not registered with the network",
        "properties": {{
          "timer_active": "T3502",
          "parameters": ["T3502"]
        }}
      }},
      {{
        "id": "node2",
        "name": "Event_InitialRegistration_Trigger",
        "type": "event",
        "description": "Initial registration trigger occurs at UE",
        "parameters": ["registration_attempt_counter"],
        "properties": {{
          "timer_trigger": false,
          "message_type": "N/A",
          "section_reference": ["5.5.1.2.2"]
        }}
      }}
    ],
    "edges": [
      {{
        "id": "edge1",
        "from": "node1",
        "to": "node2",
        "condition": [
          "Initial registration conditions met"
        ],
        "properties": {{
          "parameters": ["registration_attempt_counter"],
          "context": {{
            "emergency_service_flag": "false"
          }},
          "section_reference": ["5.5.1.2.2"]
        }}
      }},
      {{
        "id": "edge2",
        "from": "node2",
        "to": "node3",
        "condition": [
          "Initial registration conditions met"
        ],
        "action": [
          "Send REGISTRATION REQUEST",
          "Start T3510",
          "Stop T3502",
          "Stop T3511"
        ],
        "properties": {{
          "parameters": ["T3510", "T3502", "T3511"],
          "section_reference": ["5.5.1.2.2"]
        }}
      }}
    ]
  }}
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
    
    extracted_data = read_json_file("step2.json")
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
    save_to_json(procedural_info, "step3-enrich.json")
else:
    print("Failed to extract")
