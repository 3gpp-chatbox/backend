import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

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
    
    prompt = f"""Construct a structured flow graph for the procedure "{section_name}" 
based on the extracted steps and decision logic. Ensure that:

- Sequential and parallel flows are clearly represented.
- Decision nodes, timers, and retry loops are included.
- Graph abstraction layers allow both high-level and detailed views.

### Input Data:
#### Extracted Procedure Steps:
{json.dumps(step1_data, indent=2)}

#### Decision Points & Dependencies:
{json.dumps(step2_data, indent=2)}

### Example Output Format:
{{
  "graph": {{
    "nodes": [
      {{"id": 1, "type": "start", "description": "UE sends Initial Registration Request"}},
      {{"id": 2, "type": "process", "description": "AMF forwards request to SMF"}},
      {{"id": 3, "type": "decision", "description": "Is DNN supported?"}}
    ],
    "edges": [
      {{"from": 1, "to": 2, "type": "sequential"}},
      {{"from": 2, "to": 3, "type": "conditional"}}
    ]
  }}
}}"""

    response = model.generate_content(prompt).text.strip()
    return response

def save_to_json(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")

def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    step1_data = read_json_file("step1.json")
    step2_data = read_json_file("step2.json")

    if step1_data is None or step2_data is None:
        print("Failed to load step1.json or step2.json")
        return None

    procedural_info = extract_procedural_info(section_name, step1_data, step2_data)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "step3.json")
else:
    print("Failed to extract procedural information")
