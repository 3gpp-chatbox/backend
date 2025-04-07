import os
import json
from dotenv import load_dotenv
from google import genai

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
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
You are a **3GPP Procedure Flow Graph Generator**. Using the extracted structured data from **Step 1 (procedure steps, messages, state transitions, timers)** and **Step 2 (decision logic, dependencies, fallbacks, retries, and timeouts)**, construct a **Flow Property Graph (FPG)** for the procedure **"{section_name}"**.

---

## ** What to Construct (Graph-Based Representation)**

The Flow Property Graph should capture the **cause-effect relationships** between steps, messages, decisions, and timers, ensuring a structured and analyzable flow. Each node and edge in the graph must adhere to the following definitions:

### **1. Nodes (Key Elements in the Procedure Flow)**

- **Step Nodes**: Each procedural step should be a distinct node.
- **Decision Nodes**: Any decision point (e.g., timer expiry, authentication success/failure) should be a node with multiple outgoing edges for possible outcomes.
- **Message Nodes**: Key NAS messages exchanged between entities should be represented as nodes.
- **Timer Nodes**: Important timers (start, expiry) must be explicitly represented.

**Node Field Constraints:**

- **`name`**: This field MUST be a concise, short description of the node's purpose. Prioritize brevity.
- **`description`**: This field is OPTIONAL. Include it ONLY if the `name` is insufficient to convey the node's meaning, and if adding critical, non-redundant contextual information.
- **`condition` (for Decision Nodes)**: This field MUST be a short, direct question or statement reflecting the decision being made. Avoid repeating the `name` verbatim.

### **2. Edges (Cause-Effect Links)**

- **Sequential Edges**: If Step A leads directly to Step B, an edge should represent this order.
- **Decision Edges**: If a decision node has multiple outcomes, edges should point to the next appropriate steps based on those outcomes.
- **Dependency Edges**: If Step X **must** occur before Step Y (hard dependency), an explicit edge must connect them.
- **Timeout Edges**: If a timer expires and triggers a fallback/retry, an edge should show this effect.

**Edge Field Constraints:**

- **`description`**: This field is OPTIONAL. Include it ONLY if the `relation` is not self-explanatory or requires additional context. Prioritize brevity.

---

## **🔹 Output Format (Graph-Based JSON Representation)**

The extracted **Flow Property Graph (FPG)** should be structured as follows:

```json
{{
  "procedure_name": "{section_name}",
  "nodes": [
    {{
      "id": 1,
      "type": "step",
      "name": "REG_REQ sent",
      "description": "UE to AMF",
      "entity": "UE",
      "action": "send"
    }},
    {{
      "id": 2,
      "type": "message",
      "name": "REG_ACC received",
      "description": "AMF to UE",
      "from": "AMF",
      "to": "UE",
      "action": "send"
    }},
    {{
      "id": 3,
      "type": "decision",
      "name": "Auth success?",
      "condition": "Auth successful?",
      "outcomes": ["Yes", "No"]
    }},
    {{
      "id": 4,
      "type": "timer",
      "name": "T3510 start",
      "action": "start",
      "trigger": "REG_REQ sent",
      "duration": "time_value"
    }}
  ],
  "edges": [
    {{
      "from": 1,
      "to": 2,
      "relation": "triggers"
    }},
    {{
      "from": 2,
      "to": 3,
      "relation": "leads_to"
    }},
    {{
      "from": 3,
      "to": 4,
      "condition": "No",
      "relation": "fallback"
    }},
    {{
      "from": 4,
      "to": 1,
      "condition": "Timer expires",
      "relation": "retry"
    }}
  ]
}}



### Input Data:
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
def clean_json(file_path):
    """Remove Markdown-style triple backticks (```json ... ```) from the JSON file."""
    try:
        with open(file_path, "r") as f:
            raw_data = f.read()

        # Remove Markdown code block indicators (```json and ```)
        cleaned_data = raw_data.strip().replace("```json", "").replace("```", "").strip()

        # Overwrite the file with cleaned JSON
        with open(file_path, "w") as f:
            f.write(cleaned_data)

    except Exception as e:
        print(f"Error cleaning JSON: {e}")

def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    step1_data = read_json_file("v06-step1.json")
    step2_data = read_json_file("v06-step2.json")

    if step1_data is None or step2_data is None:
        print("Failed to load step1.json or step2.json")
        return None

    procedural_info = extract_procedural_info(section_name, step1_data, step2_data)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "v06-step3-complex.json")
else:
    print("Failed to extract procedural information")

if save_to_json:
   clean_json("v06-step3-complex.json")
else:
    print("Failed to clean json file")
