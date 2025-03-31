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
You are a graph generation tool. Construct a structured **flow property graph** for the procedure "{section_name}" based on the provided steps and decision logic. "Input data" is at the end of this message.

### Graph Representation:
🔹 **Flow Nodes (control the procedure's progression):**
    - Include Start, End, Process steps, and Decision points.
    - Use 'id', 'step' from the Extracted Procedure Steps to identify nodes.
    - Use 'condition' from Decision Points & Dependencies for decision nodes.
    - Include 'entity' and 'state_change' from the Extracted Procedure Steps as node properties.

🔹 **Property Nodes (modify the flow but don't control it):**
    - Include Messages, Timers, and State Changes.
    - Use 'name' and 'action' from Extracted Procedure Steps for messages and timers.
    - Use 'triggers' from Extracted Procedure Steps to show relationships between properties.

🔹 **Edges Represent:**
    - Sequential transitions, conditional paths, retry loops, timeout-based transitions.
    - Use 'depends_on' from Decision Points & Dependencies.
    - Use 'type' and 'reason' from Decision Points & Dependencies.
    - Use 'triggers' from Extracted Procedure Steps to describe the flow between nodes.

### Example Output Format (Flow Property Graph):
{{
   "nodes": [
     {{
       "id": "1",
       "description": "Step description",
       "entity": "UE",
       "state_change": "State change",
       "messages": ["Message"]
     }}
   ],
   "edges": [
     {{
       "from": "start",
       "to": "1",
       "type": "sequential",
       "properties": {{
         "trigger": "Trigger message",
         "next_action": "Next step"
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
    
    step1_data = read_json_file("step1-v4.json")
    step2_data = read_json_file("step2-v4.json")

    if step1_data is None or step2_data is None:
        print("Failed to load step1.json or step2.json")
        return None

    procedural_info = extract_procedural_info(section_name, step1_data, step2_data)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "step3-v4.json")
else:
    print("Failed to extract procedural information")
