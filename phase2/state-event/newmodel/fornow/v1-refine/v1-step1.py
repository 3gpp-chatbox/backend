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
You are a 3GPP procedure analysis expert and a large language model with strong reasoning capabilities.

Your task is to extract a **State-Event Transition Graph** from the 3GPP procedure: "{section_name}". This graph represents a high-level logical flow of the procedure, with clearly defined **States**, **Events**, and **Transitions** between them.

---

###  DEFINITIONS

1. **State**: A system condition or phase of an entity (e.g., UE, gNB, MME). These often appear with verbs like: *enters*, *is in*, *waits for*, *has completed*, *moves to*.  
    Examples: `UE_Idle`, `MME_WaitingForAuthResponse`, `UE_Attaching`

2. **Event**: A message or action that triggers a transition between states. Usually indicated by: *sends*, *receives*, *triggers*, *initiates*, *detects*.  
    Examples: `Attach_Request_Received`, `Auth_Request_Sent`, `RRC_Connection_Established`

3. **Transition**: A directed link from one state to another via an event.  
    Format: `State_A → Event_X → State_B`

---

###  THINK STEP: Extract Candidates First

Before building the final graph, **analyze the section step-by-step** and extract:

- All **possible States**: Quote the exact phrase or rephrase only if meaning is clear
- All **Events**: Capture all message exchanges or triggering actions
- Candidate **Transitions**: Where a state leads to another based on event

Rely **only on the text** provided. However, you may use 3GPP domain knowledge **to interpret terminology or infer intent** — **but not to invent missing steps**.

 If a message or state is **not clearly stated or inferable from sentence structure**, **do not include it**.

---

###  STRUCTURE CHECK RULES

- All **edges** (transitions) must go: `state → event → state`
- Do not create orphan nodes or duplicate edges
- Only include nodes/transitions explicitly stated or unambiguously implied

---

###  OUTPUT FORMAT (JSON)

**Your entire response must ONLY be a single valid JSON object** in the following format. Do not include explanation, comments, or extra text.

{{
  "procedure_name": "{section_name}",
  "graph": {{
    "nodes": [
      {{ "id": "UE_Idle", "type": "state" }},
      {{ "id": "Attach_Request_Received", "type": "event" }},
      {{ "id": "UE_Attaching", "type": "state" }}
    ],
    "edges": [
      {{
        "from": "UE_Idle",
        "to": "Attach_Request_Received",
        "type": "trigger"
      }},
      {{
        "from": "Attach_Request_Received",
        "to": "UE_Attaching",
        "type": "condition"
      }}
    ]
  }}
}}

---

###  EXAMPLE TRANSITION LINE FROM TEXT

**Spec line**: "Once the UE powers on, it sends an Attach Request to the MME."

 Extract:
- State: `UE_Powered_On`
- Event: `Attach_Request_Sent`
- Transition: `UE_Powered_On → Attach_Request_Sent → UE_Attaching`

---

### PROCEDURE SECTION

Extract the State-Event Graph below **using only the provided text**, and return ONLY the JSON object.


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
    save_procedural_info_to_json(procedural_info, "v1-step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("v1-step1.json")
else:
    print("Failed to clean json file")