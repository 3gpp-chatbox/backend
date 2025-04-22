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
You are a 3GPP procedure analysis expert. You are given **two parts of context** for the procedure "{section_name}":

1. **First Part**: The flow property graph for the procedure "{section_name}", which includes the **states**, **events**, and **transitions** **after evaluation and correction** (this part includes nodes and edges with no descriptions).
2. **Second Part**: The original **detailed section** of the 3GPP specification document that describes the procedure.

###  Your task:
Using the **states**, **events**, and **transitions** from the **first part** (the corrected flow property graph), and the **detailed content** from the **second part** (the 3GPP specification), **enrich the transitions** in the following way:

1. **Descriptions**:  
   - For **state → event transitions**: Use the format:  
     `"Trigger:short description of trigger;Condition:Key gating condition"` (e.g., `"Lower layer indicates failure/release"`).  
   - For **event → state transitions**: Use the format:  
     `"Condition:key Condition; Action:key Action"` (e.g., `"Registration attempt counter < 5 AND Not Emergency; Abort procedure, Stop T3510"`).  
     if condition doesnt exist, write as "no condition"
   - Keep descriptions **concise (≤20 words or 100 chars)** and **explicitly derived from the spec**.  

2. **Conditions/Actions**:  
   - Only include conditions/actions **explicitly stated in the spec**.  

Definition:
### Conditions :
- Logical checks or criteria that must be met for the transition to occur (e.g., `"registration attempt counter < 5"`).
### Actions:
- Actions that entity performs in response to the event and/or condition (e.g., `"Send REGISTRATION REQUEST"`).

- Do **not infer** or assume anything outside the given content.
- Do **not rename, remove, or restructure** any nodes or edges.
- Only **add** to the existing graph.
- Keep description concise — no more than 20 words or 100 characters per description.


### 💡 Example Output Format:
```json
{{
  "procedure_name": "procedure name",
  "graph": {{
    "nodes": [
      {{
        "id": "5GMM_REGISTERED_INITIATED",
        "type": "state",
        "description": "UE is in registered state with ongoing procedure."
      }},
      {{
        "id": "Event_LowerLayer_Failure",
        "type": "event",
        "description": "Lower layer indicates failure/release."
      }}
    ],
    "edges": [
      {{
        "from": "5GMM_REGISTERED_INITIATED",
        "to": "Event_LowerLayer_Failure",
        "type": "trigger",
        "description": "Trigger:Lower layer indicates failure/release; No condition"
      }},
      {{
        "from": "Event_LowerLayer_Failure",
        "to": "5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION",
        "type": "condition",
        "description": "Condition:Registration attempt counter < 5 AND Not Emergency; Action:Abort procedure, Stop T3510"
      }}
    ]
  }}
}}

How to Enrich Transitions:
For each transition, identify the trigger and the condition that causes the transition from one state to another.
Incorporate any details from the specification about why or how each transition occurs (e.g., "triggered when UE attaches", "transition happens if authentication is successful").
If no conditions or explicit triggers are provided in the spec, you may leave those parts blank, but ensure they are still logically inferred from the spec.

Strict Rule:
You must only use the provided information in the first part and second part.
Do not make any assumptions or introduce information not clearly stated in the provided text.



First Part:
States, Events, and transitions of the procedure "{section_name}" (Extracted previously):
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
            "response_schema": Graph,

          
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
