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
2. A Flow Property Graph (FPG) generated from this text for this procedure "{section_name}" on UE side only, represented as a JSON object.

Your job is to **verify and correct** the FPG based strictly on the original content.
---

## Objectives

The generated FPG must accurately represent the UE-side flow of the procedure described in "{section_name}".

## Validation Rules

This FPG must adhere to the following rules:

- **Scope:** Only include states and transitions directly related to the procedure **"{section_name}"** as described within the provided text. Consider all explicitly mentioned initial states, entry conditions, and triggers that start the procedure.
- **UE-Side Focus:** Only include UE states, UE-visible events (things that happen to the UE), and UE actions. Do not include network-side states or actions unless they are directly described as triggering a UE event (e.g., receiving a specific message).
- **No Inference:** All states, events, and transitions in the FPG must be explicitly stated in the provided 3GPP text. Do not add anything implied or inferred.

- **Nodes:**
  - **States:** Must be explicitly named UE states as they appear in the text (e.g., "5GMM-REGISTERED"). Do not invent or modify state names.
  - **Events:** Must be explicitly described UE-visible triggers (e.g., "Receive REGISTRATION REQUEST", "T3510 expires", "Lower layer failure").Do not remove valid events (e.g., "lower layer failure", "RRC release") just because they don’t match the "Receive X" or "Timer Y expires" format — as long as they are explicitly described in the text and clearly visible to the UE.

- **Edges (Transitions):**
  - Each transition described in the text should be represented by **two directed edges**: one from a state to an event, and another from that event to the subsequent state.
  - The from and to values in each edge of the "edges" array must exactly match either the "id" or the "name" of a node defined in the "nodes" array. 
  - The `section_reference` for each edge must accurately point to the 3GPP section from which the transition was derived.
  - Do not remove a transition just because its label wording is imprecise — only if the transition itself is unsupported.
  - If a procedure describes retry or failure recovery that leads the UE back to the same state, include a transition from that state to itself. This is valid as long as the loop is explicitly described in the text.



- **Edge Labels:** flexible
  - **State to Event:** The `label` should contain the key gating condition (if any) that applies to the transition, using the phrasing: "Condition". If no explicit condition is mentioned, the label should indicate "No Condition" or similar.
  - **Event to State:** The `label` should contain the key gating condition (if any) that applies to the UE's action after the event, followed by a concise summary of the key UE action(s), using the phrasing: "Condition; Action". 

- **Corrections:**
  1. **Remove** any nodes or edges that are not explicitly supported by the provided 3GPP text.
  2. **Add** any missing state-to-event and event-to-state transitions that are explicitly described in the text. Ensure each new transition has the correct `from`, `to`, `label`, and `section_reference`.ensure add prefix Event_ for event,for example:Event_LowerLayer_Failure,Event_Receive_DEREGISTRATION_REQUEST.
  3. **If a missing transition involves a state or event that is not present in the `"nodes"` array, add that missing node to the `"nodes"` array. Ensure the added node has a unique `"id"`, the correct `"name"` as it appears in the text, and the appropriate `"type"` ("state" or "event") but ensure added node is valid state or event.**
  4. Do not rephrase or modify any edge label unless it is structurally broken (i.e., missing either the event or the action).Leave all valid labels unchanged, even if they are awkwardly worded.
  5. **Ensure** that all `from` and `to` node id/names in the `"edges"` array exist in the `"nodes"` array.
  6. **Correct the `section_reference` of any edge if it does not accurately point to the 3GPP section from which the transition (and its associated information like conditions and actions) was derived.**

---

## Output Instructions

Return a corrected version of the provided JSON object in the same format as the input FPG.
**Only include valid and explicitly supported states and transitions based on the provided 3GPP text.**
**Do not include any comments or additional explanations** — output valid JSON only.
Use only the provided original 3GPP text to validate. Do not infer or invent logic.

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
