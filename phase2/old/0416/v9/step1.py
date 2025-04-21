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

Your task is to extract the **Flow Property Graph (FPG)** for this procedure  "{section_name}"**on the UE side only**, and represent it as a structured JSON object following the format defined below.

**Do not infer or assume any information beyond what is explicitly stated in the provided text.** Focus only on the information that is directly described and avoid including anything implied.

---

## Objective

Build a Flow Property Graph where:
- **Nodes** represent **UE states or events**.
    - **States:** Explicitly named UE states (e.g., "5GMM-DEREGISTERED", "5GMM-REGISTERED", "DEREGISTERED.INITIAL"). Do not invent or infer state names.
    - **Events:** UE-visible triggers such as received messages or expired timers (e.g., "Receive DEREGISTRATION REQUEST", "T3510 expires", "Lower layer failure"). Events describe occurrences that happen **to** the UE.
- **Edges** represent transitions between states and events. Each transition will be represented by **two directed edges**: one from a state to an event, and another from that event to the subsequent state.
- Each edge must include a **label** and the **3GPP section number** from which it was derived.



## Core Components to identify (UE Side Only)

### States:
- Only include explicitly named UE states (e.g., "5GMM-REGISTERED", "DEREGISTERED.INITIAL").
-  Do not invent or infer state names.

### Events :
- These are **UE-visible triggers** like messages received or timers expiring (e.g., `"Receive DEREGISTRATION REQUEST"`, `"T3510 expires"`).
- Events describe things that happen **to** the UE.


### Conditions (used in edge labels only):
- Logical checks or criteria that must be met for the transition to occur (e.g., `"registration attempt counter < 5"`).
- Include only if **explicitly described** in the specification and directly associated with the triggering event.


### Actions (used in edge labels only):
- Actions the UE performs in response to the event and/or condition (e.g., `"Send REGISTRATION REQUEST"`).
- Must be explicitly stated — no inferences allowed.

When extracting conditions, identify what the condition applies to: the transition from a state to an event, or the action taken after an event.


---

### Edge Label:
Uses simple and specific language,Keep labels concise — no more than 20 words or 100 characters per label.
extract the key actions and conditions associated with each transition,capture the essence of  what the UE fundamentally does.ensuring captures the core actions and conditions.

##for: from state to event edge label:
Includes key gating condition that applies to the transition from a state to an event.
Use structured phrasing: "Condition"
------
##for: from event to state edge label:
Includes key gating condition that applies to the action taken after an event.
Summarizes the key UE action.
Use structured phrasing: "Condition; Action"



---

Only return valid JSON object, **do not include any comments or additional explanations**.

## JSON Output Format

EXAMPLE
```json
{{
  "procedure_name": "{section_name}",
  "graph": {{
    "nodes": [
       {{
        "id": "node1",// unique node ID, after would be node2, node3, node4,...
        "name": "5GMM_REGISTERED_INITIATED",
        "type": "state"
      }},
      {{
        "id": "node2",
        "name": "Event_LowerLayer_Failure",
        "type": "event"
      }},
       {{
        "id": "node3",
        "name": "5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION",
        "type": "state"
      }}
    ],
    "edges": [
      {{
        "id": "edge1",// unique edge ID, after would be edge2, edge3,...
        "from": "5GMM_REGISTERED_INITIATED",
        "to": "Event_LowerLayer_Failure",
        "label": "Lower layer indicates failure/release",
        "section_reference": "5.4.2.1.5"
      }},
      {{
        "id": "edge2",
        "from": "Event_LowerLayer_Failure",
        "to": "5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION",
        "label": "Registration attempt counter < 5 AND Not Emergency; Abort procedure, Stop T3510, Increment registration attempt counter, Start T3511",
        "section_reference": "5.5.1.2.7"
      }},
    ]
  }}
}}

Constraints
UE-Side Only: Do not include network-side states or actions unless they directly trigger UE transitions.
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