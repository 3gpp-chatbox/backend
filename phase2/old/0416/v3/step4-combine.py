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

Here is a list of transition data between states of the 3GPP procedure "{section_name}" in JSON format. Your task is to restructure this data into a unified flow property graph.
“Use only the provided transition data. Do not assume or extend any text beyond what’s included.”

**Goal:** Construct one graph that represents the entire flow of the procedure "{section_name}". Each state or event is a **node**, and each transition is an **edge**.

- Nodes represent either:
  - **States**: from the "from" and "to" fields.
  - **Events**: from the "event" field.

- Edges represent the **flow between nodes**, and are triggered by **events, conditions, or actions**.
  - Use **conditions or actions** as the edge label where applicable.

  

**Return the result in this JSON structure:**

```json
{{
  "procedure_name": "{section_name}",
  "nodes": [
    {{
      "id": "node1",
      "name": "5GMM-DEREGISTERED",
      "type": "state",
    
    }},
    {{
      "id": "node2",
      "name": "REGISTRATION REQUEST sent",
      "type": "event",
     
    }}
    // ... other nodes
  ],
  "edges": [
    {{
      "id": "edge1",
      "from": "5GMM-DEREGISTERED",
      "to": "REGISTRATION REQUEST sent",
      "metadata": {{
        "section_reference": "5.5.1.2.2",
     
      }},
      "event": event,
      "condition": condition,
      "action": "send REGISTRATION REQUEST"
    }},
    {{
      "id": "edge2",
      "from": "REGISTRATION REQUEST sent",
      "to": "Awaiting REGISTRATION ACCEPT/REJECT",
      "metadata": {{
        "section_reference": "5.5.1.2.2",
  
      }},
      "event": null,
      "condition": null,
      "action": "start timer T3510"
    }}
    // ... other edges
  ]
}}


this is the transition data.
{extracted_data}



"""


    model_to_use = flash_model  # or pro_model depending on your requirement
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
    
    extracted_data = read_json_file("step3-detail-transition.json")
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
    save_to_txt(procedural_info, "step4-combine.json")
else:
    print("Failed to evaluate")
