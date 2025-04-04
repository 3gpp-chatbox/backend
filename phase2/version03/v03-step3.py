import os
import json
from dotenv import load_dotenv
from google import genai

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

def extract_procedural_info(section_name, step1_data, step2_data):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
You are a **graph generation tool**. Using your knowledge of 3GPP procedures but strictly based on the provided input data, construct a **structured flow property graph** for the procedure **"{section_name}"**.

---

## ** Graph Representation Rules**
**Nodes** represent:  
✔ **Procedural Steps** (e.g., UE sends request, AMF processes message).  
✔ **Decision Points** (e.g., conditions leading to different paths).  
✔ **Timers** (started/stopped due to events).  

**Edges** represent:  
✔ **Flow transitions** (sequential, conditional, retry, fallback).  
✔ **Decision paths** (if-else branches, error handling, alternative flows).  
✔ **Dependencies** (where one step is dependent on another).  

 **Strict Rule**: Extract information **only from the provided input data**. Do **not** infer or add missing details.

---

## ** Output Format (Structured JSON)**
The extracted graph must be in the following format:

```json
{{
  "graph": {{
    "nodes": [
      {{
        "id": "start",
        "type": "start",
        "description": "Procedure starts",
        "properties": {{}}
      }},
      {{
        "id": "1",
        "type": "process",
        "description": "UE sends REGISTRATION REQUEST",
        "properties": {{
          "state_change": "N/A",
          "entity": "UE",
          "messages": ["REGISTRATION REQUEST"]
        }}
      }},
      {{
        "id": "2",
        "type": "timer",
        "description": "Timer T3510 starts",
        "properties": {{
          "action": "start",
          "timeout": "5 seconds"
        }}
      }},
      {{
        "id": "3",
        "type": "decision",
        "description": "Decision based on timer expiration",
        "properties": {{
          "condition": "Timer T3510 expires",
          "outcomes": [
            {{
              "outcome": "Success",
              "next_step": 4
            }},
            {{
              "outcome": "Failure - Retry",
              "next_step": 2,
              "reason": "Timeout"
            }}
          ]
        }}
      }},
      {{
        "id": "4",
        "type": "process",
        "description": "AMF processes REGISTRATION REQUEST",
        "properties": {{
          "state_change": "5GMM-DEREGISTERED → 5GMM-REGISTERED",
          "entity": "AMF",
          "messages": ["REGISTRATION ACCEPT"]
        }}
      }}
    ],
    "edges": [
      {{
        "from": "start",
        "to": "1",
        "type": "sequential",
        "properties": {{
          "trigger": "UE sends REGISTRATION REQUEST"
        }}
      }},
      {{
        "from": "1",
        "to": "2",
        "type": "sequential",
        "properties": {{
          "trigger": "Timer T3510 starts"
        }}
      }},
      {{
        "from": "2",
        "to": "3",
        "type": "conditional",
        "properties": {{
          "condition": "Timer T3510 expires",
          "error_type": "Timeout",
          "retry_count": 3
        }}
      }},
      {{
        "from": "3",
        "to": "4",
        "type": "sequential",
        "properties": {{
          "trigger": "AMF sends REGISTRATION ACCEPT"
        }}
      }}
    ]
  }}
}}

### Input Data:
#### Extracted Procedure Steps:
{json.dumps(step1_data, indent=2)}

#### Decision Points & Dependencies:
{json.dumps(step2_data, indent=2)}



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

def save_to_json(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")

def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    step1_data = read_json_file("v03-step1-newmodel.json")
    step2_data = read_json_file("v03-step2-newmodel.json")

    if step1_data is None or step2_data is None:
        print("Failed to load step1.json or step2.json")
        return None

    procedural_info = extract_procedural_info(section_name, step1_data, step2_data)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "v03-step3-complex-newmodel.json")
else:
    print("Failed to extract procedural information")
