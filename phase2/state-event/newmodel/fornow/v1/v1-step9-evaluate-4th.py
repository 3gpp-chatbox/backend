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
You are a 3GPP procedure expert.

You are given:
1. An **extracted flow property graph** (state-event model) for the 3GPP procedure "{section_name}".
2. The **original 3GPP specification content** from which this graph was extracted.

### Your task:
Provide a **direct and actionable correction** for the flow property graph, focusing on:
- **Missing or incorrectly modeled states, events, or transitions**.
- **Incorrectly classified states or events** (e.g., a state marked as an event).
- **Edges with wrong types** (e.g., 'condition' instead of 'trigger').

Please return **all corrections you find**, not limited to three, in the following format:

### Output Format:

```json
{{
  "corrections": [
    {{
      "type": "missing_state",
      "state": "UE_Securing",
      "description": "State 'UE_Securing' is missing after authentication.",
      "suggested_location": "After state 'UE_Authenticated' before 'UE_Attaching'."
    }},
    {{
      "type": "incorrect_event",
      "state": "Attach_Request",
      "event": "timeout",
      "suggested_correction": "The event 'Attach_Request_Timeout' should be added to the flow after the timeout timer (T3550)."
    }},
    {{
      "type": "incorrect_edge_type",
      "edge": "Attach_Request → UE_Attaching",
      "current_type": "condition",
      "suggested_type": "trigger",
      "description": "Edge 'Attach_Request → UE_Attaching' should be a 'trigger', not a 'condition'."
    }}
      // More corrections can be added as needed
  ]
}}

Flow Property Graph JSON (extracted):
{json.dumps(extracted_data, indent=2)}

------------------

#### **Original Content from 3GPP Specification:**  
{original_content}

**Strict Rule**: 
Rely **solely** on the provided content for corrections. Do not make assumptions or introduce information beyond the provided text.

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
    
    extracted_data = read_json_file("v1-step8-correct-3rd.json")
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
    save_to_txt(procedural_info, "v1-step9-evaluate-4th.json")
else:
    print("Failed to evaluate")
