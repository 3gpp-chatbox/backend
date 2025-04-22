# Primary authentication and key agreement procedure - TXT file version
import os
from dotenv import load_dotenv
from google import genai
import json

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


def extract_procedural_info_from_text(section_name, text):
    prompt = f"""

You will be provided with original content from 3GPP specification sections describing the procedure: "{section_name}".
Your task is to extract the **Flow Property Graph (FPG)** for this procedure "{section_name}", and represent it as a structured JSON object following the format defined below.
**Do not infer or assume any information beyond what is explicitly stated in the provided text.** Focus only on the information that is directly described and avoid including anything implied.

---

## Objective

Build a Flow Property Graph where:
- **Nodes** represent **states or events** for all entities involved (UE, AMF, etc.)
  - **States:** Explicitly named states for any entity (e.g., "5GMM-DEREGISTERED", "AMF_REGISTERED_STATE"). Do not invent or infer state names.
  - **Events:** Visible triggers such as received messages or expired timers (e.g., "Receive DEREGISTRATION REQUEST", "T3510 expires", "Lower layer failure"). Events describe occurrences/triggers that happen.
  
- **Edges** represent transitions between states and events. Each transition will be represented by **two directed edges**:
  - One from a state to an event
  - One from that event to the subsequent state
  
- Each edge must include a specific **type**:
  - "trigger": From state to event (state is triggered by event)
  - "condition": From event to state (event leads to state under conditions)
  
- **Edge Type Notes**:
  - All event→state transitions inherently represent actions, but currently map these to `"condition"` type edges
   
- Each node must be clearly identified with its entity type (UE or network entity) in node name, like "UE_5GMM_REGISTERED", "AMF_WAITING_FOR_AUTH".
- For all event nodes, names should have prefix Event_, like Event_LowerLayer_Failure.

---

## Core Components to identify (All Entities)

### States:
- Include explicitly named states for all entities (UE, AMF, etc.)
- Format: "[ENTITY]_[STATE_NAME]" (e.g., "UE_5GMM_REGISTERED", "AMF_WAITING_FOR_AUTH")
- Do not invent or infer state names.

### Events:
- These are **visible triggers** like messages received or timers expiring (e.g., `"Receive DEREGISTRATION REQUEST"`, `"T3510 expires"`).
- Include events for all entities involved.

### Conditions:
- Logical checks or criteria that must be met for the transition to occur (e.g., `"registration attempt counter < 5"`).
- Include only if **explicitly described** in the specification and directly associated with the triggering event.

### Actions:
- Actions the entity performs in response to the event and/or condition (e.g., `"Send REGISTRATION REQUEST"`).
- Must be explicitly stated — no inferences allowed.

### Conditions and Actions:
- You may identify conditions and actions during analysis, but only include them as edge types in the final JSON
- Do not include condition/action details in the final output

---

## JSON Output Format

```json
{{
  "procedure_name": "{section_name}",
  "graph": {{
    "nodes": [
      {{"id": "UE_5GMM_REGISTERED_INITIATED", "type": "state"}},
      {{"id": "Event_LowerLayer_Failure", "type": "event"}},
      {{"id": "UE_5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION", "type": "state"}},
      {{"id": "AMF_REGISTRATION_PENDING", "type": "state"}}
    ],
    "edges": [
      {{
        "from": "UE_5GMM_REGISTERED_INITIATED",
        "to": "Event_LowerLayer_Failure",
        "type": "trigger"
      }},
      {{
        "from": "Event_LowerLayer_Failure",
        "to": "UE_5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION",
        "type": "condition"
      }},
      {{
        "from": "AMF_REGISTRATION_PENDING",
        "to": "Event_Receive_REGISTRATION_REQUEST",
        "type": "trigger"
      }}
    ]
  }}
}}
Constraints
Multiple Entities: Include states and events for all entities involved (UE, AMF, etc.)
No Inference: Use only information that is explicitly stated in the input content.
Multiple Paths: If the spec describes alternate paths (e.g., emergency mode, failure recovery), include them all.
Fallbacks and Edge Cases: Capture fallback or error handling flows if explicitly described.
Support for Self-loops: If a procedure describes retry or failure recovery that leads the UE back to the same state, include a transition from that state to itself. This is valid as long as the loop is explicitly described in the text.
Input Text:
Analyze only the content below. Do not reference external knowledge:
{text}
"""


    model_to_use = new_model  # or pro_model depending on your requirement
    response = client.models.generate_content(
        model=model_to_use,
        contents=prompt,
        config={
            "temperature": 0,
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
    save_procedural_info_to_json(procedural_info, "step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1.json")
else:
    print("Failed to clean json file")