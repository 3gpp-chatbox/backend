import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

flash_model = "gemini-2.0-flash"
pro_model = "gemini-2.0-pro-exp-02-05"

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
    prompt = f"""
You are a graph generation tool. Construct a structured ** flow property graph **  for the procedure "{section_name}" based on the provided steps and decision logic(whici is "input data" in the end of this message).

Represent:

-   The sequence of steps as nodes, including their descriptions and any relevant properties (e.g., state changes, involved entities).
-   The flow between steps as edges, including their types (sequential, conditional, retry) and any associated conditions.
-   Decision points and timers as specific node types, with their conditions and properties.
-   Dependencies and conditions as edge properties, along with possible fallback actions.

Create a graph that is easy to understand, showing the main flow and any alternative paths, with detailed properties for each node and edge.


### example Output Format:
{{
  "nodes": [
    {{
      "id": "start",
      "type": "start",
      "description": "Procedure starts",
      "properties": {{
        "entity": "UE",
        "state_change": "N/A"
      }}
    }},
    {{
      "id": "1",
      "type": "process",
      "description": "UE sends REGISTRATION REQUEST",
      "properties": {{
        "entity": "UE",
        "state_change": "N/A",
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
      "type": "process",
      "description": "AMF processes REGISTRATION REQUEST",
      "properties": {{
        "entity": "AMF",
        "state_change": "5GMM-DEREGISTERED to 5GMM-REGISTERED",
        "messages": ["REGISTRATION ACCEPT"]
      }}
    }},
    {{
      "id": "4",
      "type": "process",
      "description": "UE receives REGISTRATION ACCEPT",
      "properties": {{
        "entity": "UE",
        "state_change": "5GMM-DEREGISTERED to 5GMM-REGISTERED",
        "messages": ["REGISTRATION COMPLETE"]
      }}
    }}
  ],
  "edges": [
    {{
      "from": "start",
      "to": "1",
      "type": "sequential",
      "properties": {{
        "trigger": "UE sends REGISTRATION REQUEST",
        "message": "REGISTRATION REQUEST",
        "next_action": "Wait for REGISTRATION ACCEPT"
      }}
    }},
    {{
      "from": "1",
      "to": "2",
      "type": "sequential",
      "properties": {{
        "trigger": "Timer T3510 starts",
        "timeout": "5 seconds",
        "next_action": "Proceed with step 2 after timeout"
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
        "message": "REGISTRATION ACCEPT",
        "trigger": "AMF sends REGISTRATION ACCEPT",
        "next_action": "Proceed to step 4"
      }}
    }}
  ]
}}


### provided Input Data:
#### Extracted Procedure Steps:
{json.dumps(step1_data, indent=2)}

#### Decision Points & Dependencies:
{json.dumps(step2_data, indent=2)}


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


def save_to_json(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")

def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    step1_data = read_json_file("step1-v3.json")
    step2_data = read_json_file("step2-v3.json")

    if step1_data is None or step2_data is None:
        print("Failed to load step1.json or step2.json")
        return None

    procedural_info = extract_procedural_info(section_name, step1_data, step2_data)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "step3-v3.json")
else:
    print("Failed to extract procedural information")
