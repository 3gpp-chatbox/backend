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

Your task is to extract the **Flow Property Graph (FPG)** for this procedure **on the UE side only**, and represent it as a structured JSON object using the format defined below.

**Do not infer or assume any information beyond what is explicitly described in the provided text.**

---

##  Objective

Build a **Flow Property Graph (FPG)** where:

- **Nodes** represent one of the following **UE-side elements only**:
    - **States**: Explicitly named UE states (e.g., `"5GMM-DEREGISTERED"`, `"CM-IDLE"`).
    - **Conditions**: Logical checks or criteria that must be met for transitions (e.g., `"registration attempt counter < 5"`). Include only if **explicitly described** in the text.
    - **Decisions/Actions**: Explicit actions or decisions by the UE (e.g., `"Send REGISTRATION REQUEST"`). Must be **explicitly described** in the spec.

- **Edges** represent **events or triggers** that cause transitions between nodes.
    - Events are **not nodes**.
    - Instead, represent each trigger as the **label of the edge** that connects two nodes.
    - Each edge must include:
        - A **label** describing the event or trigger (e.g., `"T3510 expires"`, `"Receive DEREGISTRATION REQUEST"`)
        - The **3GPP section number** it was derived from

---

##  Definitions and Extraction Rules (UE Side Only)

###  States
- Include only **explicitly named** UE states
- Do **not infer or invent** any state names

###  Events (Triggers)
- External occurrences **visible to the UE** that initiate transitions (e.g., `"T3510 expires"`, `"Receive IDENTITY REQUEST"`, `"Lower layer failure"`)
- Represent these only as **edge labels**
- Events **must not be modeled as nodes**

###  Conditions
- Logical checks that gate a transition (e.g., `"registration attempt counter < 5"`)
- Only include if **explicitly mentioned** in the text

###  Actions / Decisions
- Actions taken **by the UE** (e.g., `"Abort procedure"`, `"Send REGISTRATION REQUEST"`)
- Only include if **explicitly stated**

---

##  Output Format (JSON)

Return only a valid JSON object, **no extra text or comments**.

```json
{{
  "procedure_name": "{section_name}",
  "graph": {{
    "nodes": [
      {{
        "id": "node1",
        "name": "5GMM_REGISTERED_INITIATED",
        "type": "state"
      }},
      {{
        "id": "node2",
        "name": "registration attempt counter < 5 AND Not Emergency",
        "type": "condition"
      }},
      {{
        "id": "node3",
        "name": "Abort procedure, Stop T3510, Increment registration attempt counter, Start T3511",
        "type": "action"
      }},
      {{
        "id": "node4",
        "name": "5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION",
        "type": "state"
      }}
    ],
    "edges": [
      {{
        "id": "edge1",
        "from": "5GMM_REGISTERED_INITIATED",
        "to": "registration attempt counter < 5 AND Not Emergency",
        "label": "Event: Lower layer indicates failure/release",
        "section_reference": "5.4.2.1.5"
      }},
      {{
        "id": "edge2",
        "from": "registration attempt counter < 5 AND Not Emergency",
        "to": "Abort procedure, Stop T3510, Increment registration attempt counter, Start T3511",
        "label": "Condition met",
        "section_reference": "5.5.1.2.7"
      }},
      {{
        "id": "edge3",
        "from": "Abort procedure, Stop T3510, Increment registration attempt counter, Start T3511",
        "to": "5GMM_DEREGISTERED_ATTEMPTING_REGISTRATION",
        "label": "Action complete",
        "section_reference": "5.5.1.2.7"
      }}
    ]
  }}
}}

Constraints
UE-Side Only: Do not include network-side behavior unless it directly triggers UE-side transitions.

No Inference: Use only information explicitly stated in the source text.

Multiple Paths: Capture all explicitly described branches (e.g., retries, failure recovery, emergency mode).

Self-loops Allowed: Include loops only if explicitly described (e.g., retry behavior leading back to same state).

Traceability Required: Every edge must reference a 3GPP section number.

Input Text:
Analyze only the content below. Do not reference external knowledge: 
{text} """




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