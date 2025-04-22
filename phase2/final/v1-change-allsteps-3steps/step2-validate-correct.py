import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

load_dotenv()

flash_model = "gemini-1.5-flash"
pro_model = "gemini-2.0-pro-exp-02-05"
new_model = "gemini-2.5-pro-exp-03-25"
flash_20 = "gemini-2.0-flash"

# Load the Google API Key from the .env file
load_dotenv(override=True)


# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. Please set it in your .env file."
    )

client = genai.Client(api_key=api_key)



def read_json_file(file_path):
    """Reads content from a JSON file and returns the parsed JSON object."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
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
You are given two inputs:

1. The original content from a 3GPP specification section describing the procedure: "{section_name}".
2. A Flow Property Graph (FPG) generated from this text for all involved entities (UE, AMF, etc.), represented as a JSON object.

Your job is to **validate and correct** this FPG strictly based on the original 3GPP content provided.

---

## Objectives

Ensure the FPG accurately represents the **complete multi-entity flow** of the procedure described in "{section_name}", using **only** information that is explicitly stated in the provided content.

---

## Validation Rules

### General Rules:
- **Do not infer** or add any states, events, transitions, or entities unless explicitly described in the text.
- **Only include** nodes and transitions directly related to the specified procedure in this section.
- Ensure **clarity of entity ownership** in node IDs (e.g., "UE_", "AMF_").

### Nodes: 
- **States:** 
  - Must be explicitly named and associated with the correct entity.
  - Use format: `"ENTITY_STATENAME"` (e.g., `"UE_5GMM_REGISTERED"`).
- **Events:**
  - Must represent **visible triggers**: received messages, timer expiries, or errors.
  - Must have names prefixed with `"Event_"` (e.g., `"Event_Receive_REGISTRATION_REQUEST"`).
- **Do not invent names.** Only include those directly stated in the specification.

### Edges:
- Every transition must be represented by **two edges**:
  1. **Trigger edge**: from a state to an event (`"type": "trigger"`).
  2. **Condition or action edge**: from the event to the resulting state (`"type": "condition"` or `"type": "action"`).
- All `from` and `to` values in the `"edges"` array must match the `"id"` of a node defined in the `"nodes"` array.

### Corrections:
1. **Remove** any unsupported nodes or edges.
2. **Add** any missing state-event-state transitions described in the spec.
3. **If a referenced node is missing from the nodes array, add it.** Make sure to:
   - Set `"id"` using exact name from spec with correct prefix.
   - Set `"type"` to `"state"` or `"event"`.
4. **Ensure edge types** (`"trigger"`, `"condition"`, `"action"`) are correct based on the role of the transition.
5. Handle retry/self-loop cases only if explicitly stated.

---

## Output Instructions

Return the corrected JSON object in the same structure as the input.

- Do not include any comments or explanations.
- Only include states, events, and transitions explicitly described in the original specification.
- Ensure all IDs used in edges exist in the nodes list.
- The final output must be a valid JSON object.

---

### Input FPG to validate and correct:

{extracted_data}

---

### Original Specification Content (ground truth):

{original_content}
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

def save_to_txt(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")



def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    extracted_data = read_json_file("step1.json")
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
    save_to_txt(procedural_info, "step2.json")
else:
    print("Failed to evaluate")
