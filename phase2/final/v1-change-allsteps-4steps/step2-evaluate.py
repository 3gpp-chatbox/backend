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
You are given two inputs:

1. The original content from a 3GPP specification section describing the procedure: "{section_name}".
2. A Flow Property Graph (FPG) generated from this text for all involved entities (UE, AMF, etc.), represented as a JSON object.

Your task is to **evaluate and validate** the FPG based only on the original content. **Do not return a corrected FPG. Instead, return a detailed evaluation report.**

---

## Evaluation Objectives

Assess whether the provided FPG is an accurate, complete, and explicit representation of the procedure as described in the text.

---

## Evaluation Criteria

### 1. Node Validation
- Identify any **missing** or **extra** nodes (states/events).
- **Nodes:**
  - **States:** Must be explicitly named UE states as they appear in the text (e.g., "5GMM-REGISTERED"). Do not invent or modify state names.
  - **Events:** Must be explicitly described visible triggers (e.g., "Receive REGISTRATION REQUEST", "T3510 expires", "Lower layer failure").Do not remove valid events (e.g., "lower layer failure", "RRC release") just because they don’t match the "Receive X" or "Timer Y expires" format — as long as they are explicitly described in the text and clearly visible to the UE.

- Verify all node IDs:
  - States: Must be explicitly named and prefixed with the correct entity (e.g., `"UE_"`, `"AMF_"`).
  - Events: Must begin with `"Event_"` and be clearly described in the spec (e.g., message received, timer expiry).
- Flag any node not directly supported by the original content.

### 2. Edge Validation
- Each valid transition must consist of **two edges**:
  - A `trigger` edge from a state to an event.
  - A `condition` edge from that event to a state.
- Verify:
  - Both `from` and `to` values match a node `id` in the `"nodes"` list.
  - Edge types are used correctly.
  - Transitions are explicitly stated in the input text.

  - **Edges (Transitions):**
  - Each transition described in the text should be represented by **two directed edges**: one from a state to an event, and another from that event to the subsequent state.
  - Do not remove a transition just because its type is imprecise — only if the transition itself is unsupported.
  - If a procedure describes retry or failure recovery that leads the UE back to the same state, include a transition from that state to itself. This is valid as long as the loop is explicitly described in the text.Some transitions may involve multiple conditions/actions or parallel paths.
  - All edge from event to state exist action in procedure, but for now, we just keep this kind of edge type "condition"
  - Confirm all event→state edges use `"condition"` type (even when representing actions)

### 3. Transition Coverage
- Identify **missing transitions** that are described in the text but not represented in the FPG.
- Identify **redundant or invalid transitions** that are not supported by the text.

- Do not remove a transition just because its type is imprecise — only if the transition itself is unsupported.
  - If a procedure describes retry or failure recovery that leads the UE back to the same state, include a transition from that state to itself. This is valid as long as the loop is explicitly described in the text.
---

## Output Format

Return a JSON object in the following format:

```json
{{
  "summary": {{
    "valid": true/false,
    "missing_nodes": [{{"id": "...", "reason": "...","suggested_correction": "..."}}, ...],
    "invalid_nodes": [{{"id": "...", "reason": "...","suggested_correction": "..."}}, ...],
    "extra_nodes": [{{"id": "...", "reason": "...","suggested_correction": "..."}}, ...],
    "missing_edges": [{{"from": "...", "to": "...", "type": "...", "reason": "...","suggested_correction": "..."}}, ...],
    "invalid_edges": [{{"from": "...", "to": "...", "type": "...", "reason": "...","suggested_correction": "..."}}, ...]
  }},
  "comments": [
    "Observation or warning about structure or logic",
    ...
  ]
}}

Only use the input content to validate — do not infer or assume.
Return all issues you find, no matter how small.
Maintain valid JSON structure for all responses.
return ONLY the valid JSON object.


Input FPG:
{extracted_data}

Original Text:
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
    
    extracted_data = read_json_file("v1-step1.json")
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
    save_to_txt(procedural_info, "v1-step2-evaluate.json")
else:
    print("Failed to evaluate")
