# Primary authentication and key agreement procedure - TXT file version
import os
from dotenv import load_dotenv
from google import genai
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
  

class Edge(BaseModel):
    """Represents a Trigger or Condition connecting Nodes"""
    from_node: str = Field(..., alias="from", description="ID of the starting node.")
    to: str = Field(..., description="ID of the target node.")
    type: str = Field(..., description="Type of the edge, either 'trigger' or 'condition'.")
   

class Graph(BaseModel):
    """Graph structure containing all States, Events, Triggers, and Conditions"""
    nodes: List[Node] = Field(..., description="List of all states and events.")
    edges: List[Edge] = Field(..., description="List of all triggers and conditions.")



def extract_procedural_info_from_text(section_name, text):
    prompt = f"""
You are a 3GPP procedure analysis expert and a large language model with strong reasoning capabilities.

Your task is to extract a **detailed State-Event Transition Graph** from the 3GPP procedure: "{section_name}". This graph represents the **complete logical flow**, including both **high-level phases** and **detailed protocol steps**, using clearly defined **States**, **Events**, and **Transitions**.

---

###  DEFINITIONS (Expanded for Detailed Mode)

1. **State**: A system condition, behavioral phase, or protocol step of an entity (e.g., UE, gNB, AMF). These may include:
    - Operational states: `UE_Idle`, `gNB_Connected`
    - Transient protocol states: `WaitingForRRCConnection`, `Authenticating`, `SecurityModeSetupPending`
    - Buffering or waiting: `MME_WaitingForAuthResponse`, `UE_WaitingForAttachAccept`

2. **Event**: A message exchange or action that triggers a change in state. Look for:
    - NAS/RRC/S1AP messages: `Attach_Request_Sent`, `Auth_Challenge_Received`, `SecurityModeCommand_Sent`
    - Internal triggers or responses: `Authentication_Successful`, `Timer_T3410_Expired`

3. **Transition**: A directional change in system state triggered by an event.
    Format: `State_A → Event_X → State_B`

---

###  THINKING MODE: Detailed Extraction

- Read the procedure **step-by-step**.
- Extract **ALL identifiable states and events**, from both high-level flow and protocol internals.
- Capture **fine-grained transitions**, including intermediate signaling and waiting phases.
- Use 3GPP knowledge to **interpret terminology**, **but do not invent transitions** not logically implied by the text.

---

### 🛠 STRUCTURE RULES (Strict)

- Each transition must follow: `state → event → state`
- No orphaned states or events.
- Only include nodes and transitions **explicitly described or logically inferable** from text.
- Avoid duplications.

---

###  OUTPUT FORMAT (JSON only)
**Your entire response must ONLY be a single valid JSON object** in the following format. Do not include explanation, comments, or extra text.

```json
{{
  "procedure_name": "{section_name}",
  "graph": {{
    "nodes": [
      {{ "id": "UE_Idle", "type": "state" }},
      {{ "id": "RRC_Connection_Request_Sent", "type": "event" }},
      {{ "id": "UE_WaitingForRRCSetup", "type": "state" }}
    ],
    "edges": [
      {{
        "from": "UE_Idle",
        "to": "RRC_Connection_Request_Sent",
        "type": "trigger"
      }},
      {{
        "from": "RRC_Connection_Request_Sent",
        "to": "UE_WaitingForRRCSetup",
        "type": "condition"
      }}
    ]
  }}
}}
 EXAMPLES FROM TEXT
Spec line: "The UE sends an RRC Connection Request to establish signaling."

Extract:
State: UE_Idle
Event: RRC_Connection_Request_Sent
State: UE_WaitingForRRCSetup
Transition: UE_Idle → RRC_Connection_Request_Sent → UE_WaitingForRRCSetup

PROCEDURE SECTION
Now extract the detailed State-Event Transition Graph below, using only the provided text. Return ONLY the JSON object.

{text}



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

def save_procedural_info_to_json(procedural_info, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(procedural_info)
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

def process_text_file(input_file_path, section_name):
    """Processes content from a text file instead of database."""
    text_content = read_text_file(input_file_path)
    if text_content is None:
        return None
        
    procedural_info = extract_procedural_info_from_text(section_name, text_content)
    return procedural_info

# Example usage: Processing a text file
input_file_path = "5.5.1.2.txt"  # Path to your input text file
section_name = "Registration procedure for initial registration"  # Name of the section/procedure

procedural_info = process_text_file(input_file_path, section_name)

if procedural_info:
    save_procedural_info_to_json(procedural_info, "v1-step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("v1-step1.json")
else:
    print("Failed to clean json file")