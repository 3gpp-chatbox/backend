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

def extract_procedural_info(section_name, extracted_data, evaluation):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
You are given the following inputs:

1. A Flow Property Graph (FPG) in JSON format for the procedure "{section_name}".
2. An evaluation report identifying missing or incorrect nodes and edges in the FPG.

Your task is to **correct the FPG** using the evaluation report provided.

---

## Correction Instructions

Using the evaluation report, update the FPG:

- **Add missing nodes or edges** that are explicitly described in the text.
- **Remove invalid or extra nodes and edges** that are not supported by the content.
- **Ensure consistency** between all `from`/`to` values in edges and `id`s in the node list.
- **Edge Types**:
  - State→event must be `"trigger"`
  - Event→state must be `"condition"` (note: these transitions always represent actions in the actual procedure)
- **Node names and structure** must follow:
  - States: `"ENTITY_STATE_NAME"` (e.g., `"UE_5GMM_DEREGISTERED"`)
  - Events: `"Event_[EVENT_DESCRIPTION]"` (e.g., `"Event_T3510_Expires"`)

---

## Output Instructions

Return a single corrected FPG JSON object with the same structure as the input.

- Do not include the evaluation report.
- Do not include comments or explanations.
- Use only data supported by the original text.
- Do **not** invent new states, events, or transitions beyond those described.
- Do **not** make assumptions or corrections that are not supported by the evaluation.

---

###  Output Format (JSON):
Return ONLY the corrected graph in this format:

```json
{{
  "procedure_name": "{section_name}",
  "graph": {{
    "nodes": [...],
    "edges": [...]
  }}
}}

---
STRICT RULE: Return **only** a valid JSON object. No commentary, no explanation, no text before or after the JSON.


#### **Extracted procedure flow property graph info:**  

{json.dumps(extracted_data, indent=2)}

------------------
#### **Evaluation Report:**  
{evaluation}

"""


    model_to_use = new_model  # or pro_model depending on your requirement
    response = client.models.generate_content(
        model=model_to_use,
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json",
          
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



def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    extracted_data = read_json_file("v1-step1.json")
    evaluation = read_text_file("v1-step2-evaluate.json")

    if extracted_data is None or evaluation is None:
        print("Failed to load extracted_data or evaluation")
        return None

    procedural_info = extract_procedural_info(section_name, extracted_data, evaluation)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "v1-step3-correct.json")
else:
    print("Failed to correct")
