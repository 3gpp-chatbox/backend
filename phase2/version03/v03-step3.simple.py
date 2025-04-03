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

def extract_procedural_info(section_name, step1_data, step2_data):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
  You are a **graph generation tool**. Your task is to construct a **state-event flow property graph** for the procedure **"{section_name}"**, based on structured data extracted in previous steps(in the end of this message).

  ---

## **Input Data Sources**  
✔ **Step 1 JSON** → Extracted high-level flow, including:  
   - **Steps** (key procedural actions)  
   - **Messages** (signaling interactions)  
   - **State Transitions** (e.g., "Idle → Registered")  
   - **Timers** (e.g., "T3510 starts")  
   - **Entities** (e.g., UE, AMF, gNB)  

✔ **Step 2 JSON** → Extracted decision logic, including:  
   - **Conditional branching** (e.g., "If authentication fails, retry 3 times")  
   - **Dependencies** (e.g., "Step A must happen before Step B")  
   - **Fallback conditions** (e.g., "If network unavailable, trigger reattempt")  

---

## **Graph Representation Rules**  
### **1. States (Nodes)**  
- Represent different stages in the process (e.g., **"UE Registered"**, **"Authentication Successful"**).  
- Each state should include:  
  - **Unique identifier** (`id`)  
  - **Description** (`description`)  
  - **Message (if applicable)** (`message`)  
  - **Type** (`state` or `event`)  

#### Example:  
```json
{{
  "id": "state1",
  "type": "state",
  "description": "UE Registered",
}}
   2. Triggers and Conditions (Edges)
Represent the relationships between states.
Each edge should include:
Starting node (from)
Target node (to)
Type (trigger or condition)
Description (description)
Example:
{{
  "from": "state1",
  "to": "state2",
  "type": "trigger",
  "description": "Authentication Success"
}}


Example Output Format (Structured JSON)

{{
  "procedure_name": "Procedure Name Here",
  "description": "Description Here",
  "graph": {{
    "nodes": [
      {{
        "id": "state1",
        "type": "state",
        "description": "UE Registered"
      }},
      {{
        "id": "event1",
        "type": "event",
        "description": "UE Sends Registration Request"
      }}
    ],
    "edges": [
      {{
        "from": "state1",
        "to": "event1",
        "type": "trigger",
        "description": "Power On"
      }},
      {{
        "from": "event1",
        "to": "state2",
        "type": "condition",
        "description": "Authentication Success"
      }}
    ]
  }}
}}

 **Strict Rule**: Use **only** the provided JSON data from Step 1 and Step 2. Do **not** infer or add missing details.

### Provided JSON Input:
#### Step 1: High-Level Flow Extracted:
{json.dumps(step1_data, indent=2)}

#### Step 2: Decision Logic & Dependencies
{json.dumps(step2_data, indent=2)}

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

def clean_json(file_path):
    """Remove Markdown-style triple backticks (```json ... ```) from the JSON file."""
    try:
        with open(file_path, "r") as f:
            raw_data = f.read()

        # Remove Markdown code block indicators (```json and ```)
        cleaned_data = raw_data.strip().replace("```json", "").replace("```", "").strip()

        # Overwrite the file with cleaned JSON
        with open(file_path, "w") as f:
            f.write(cleaned_data)

    except Exception as e:
        print(f"Error cleaning JSON: {e}")

def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    step1_data = read_json_file("v03-step1-newmodel.json")
    step2_data = read_json_file("v03-step2-newmodel.json")

    if step1_data is None or step2_data is None:
        print("Failed to load step1.json or step2.json")
        return None

    procedural_info = extract_procedural_info(section_name, step1_data, step2_data)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "v03-step3-simple-newmodel.json")
else:
    print("Failed to extract procedural information")
if save_to_json:
   clean_json("v03-step3-simple-newmodel.json")
else:
    print("Failed to clean json file")