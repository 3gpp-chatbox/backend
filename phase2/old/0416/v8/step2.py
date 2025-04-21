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
2. A Flow Property Graph (FPG) generated from this text for this procedure "{section_name}" on UE side only.

Your job is to **verify and correct** the FPG based strictly on the original content. 

---

## Objectives

## Validation Rules

This FPG must reflect:
- Only the procedure **"{section_name}"**
- Consider all content within the sections "{section_name}" as part of the procedure — including any initial states, entry conditions, or triggers that start the procedure.
- Only the **UE-side behavior**, unless it directly involves a message **received by the UE**.


- **States**:
  - Must match UE states explicitly mentioned in the text.
  - No invented or inferred state names allowed.

- **Transitions (Edges)**:
  - Must describe an explicitly defined change in UE state.
  - Do not remove a transition just because its label wording is imprecise — only if the transition itself is unsupported.
  - Event and action must both be present in the label:
    - **Event**: Something that happens to the UE and triggers a transition (e.g., "Receive X", "Timer Y expires", "Lower layer failure"). Must be explicitly described in the spec.
 Do not remove transitions with valid events (e.g., "lower layer failure", "RRC release") just because they don’t match the "Receive X" or "Timer Y expires" format — as long as they are explicitly described in the text and clearly visible to the UE.
    - **Action**: What the UE does in response (e.g., "Send Z", "Start timer")
  - Label format should use `—` to separate event/condition from action.
  


- Correct any issues:
1. **Remove** invented or unsupported states or transitions.
2. **Add** any missing transitions that are clearly and explicitly described in the input text.
3. **Fix** labels that are missing either the event or the action.
Do not rephrase or modify any edge label unless it is structurally broken (i.e., missing either the event or the action).
Leave all valid labels unchanged, even if they are awkwardly worded.


---

## Labeling Rules Recap

- **Events**: What happens to the UE (e.g., receive message, timer expires).
- **Conditions**: Any gating logic (e.g., counter < 5), if stated.
- **Actions**: What the UE does (e.g., send message, initiate retry).
- **Label Limit**: Max 20 words or 100 characters.

Use phrasing: `"[Event], [Condition] — [Action]"`

---

## Output Instructions

Return a corrected version of the JSON object below in the same format as defined in Step 1.  
**Only include valid and explicitly supported states and transitions**.  
**Do not explain or comment on the changes** — output valid JSON only.
Use only provided original 3GPP text to validate. Do not infer or invent logic.
Focus on correct transitions, not perfect phrasing.

---

### Input FPG (to validate and correct):

{extracted_data}

---

### Input Text (ground truth):

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
