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
You are a 3GPP procedure analysis expert and logic validator.

You are given:
1. A **flow property graph** (state-event-transition model) extracted from the 3GPP procedure: "{section_name}".
2. The **original 3GPP specification section text** from which the graph was generated.

---

###  Your task:
Evaluate the **accuracy and completeness of the high-level flow** represented in the graph, as compared to the original 3GPP text.

This graph is intended to capture **major phases and control message transitions**, not all fine-grained or internal protocol steps.

---

### What to Detect (within high-level flow only):

1. **Missing components**:
   - Key States, Events, or Transitions that are clearly described and necessary to represent the main control logic or progression of the procedure.
   - Do **not** flag minor state shifts or low-level message exchanges unless they play a **central role** in the overall flow.
2. **Incorrect components**:
   - Wrong classifications (e.g., event misclassified as state).
   - Mislabeling of clearly-defined key concepts.
3. **Incorrect edge types**:
   - `trigger` used where `condition` is more appropriate, or vice versa — **only if it alters the meaning** of the flow.
4. **Conflicting node types**:
   - Same node appears as both a state and an event.
5. **Invalid graph structure**:
   - `from` or `to` fields in edges that do not match any node `id`.
6. **Fatal errors**:
   - The graph is fundamentally invalid, or fails to capture the essential top-level transitions.

---

### Special Evaluation Scope:

- This graph is **not expected to be exhaustive**.
- Only evaluate the **core flow** — steps that reflect the structural progression of the procedure (e.g., "UE sends request → network authenticates → session established").
- **Do not flag missing steps** that are:
  - Minor protocol details.
  - Internal actions without outward transitions.
  - Nested within a broader state that is already captured.
Use your domain knowledge to judge **what constitutes a top-level transition** in typical 3GPP procedures.

---

### Reasoning Process (Do not return):

- Read the spec section line by line.
- Identify the main states and transitions implied by temporal or causal language.
- Compare to the graph, checking only that the **essential flow** is accurately represented.
- Ignore small sub-transitions unless they affect the top-level logic.

---

### Output Format (JSON)

ONLY Return a list of corrections and inconsistencies in JSON format, like this:

```json
{{
  "corrections": [
    {{
      "type": "missing_state",
      "state": "UE_Securing",
      "description": "State 'UE_Securing' is missing after successful authentication.",
      "suggested_location": "After 'UE_Authenticated' and before 'UE_Attaching'.",
      "supporting_text_snippet": "After successful authentication, the UE secures its connection before proceeding."
    }},
    {{
      "type": "incorrect_event",
      "event": "Attach_Request",
      "suggested_event": "Attach_Request_Received",
      "description": "The event 'Attach_Request' should reflect that it's received by the MME.",
      "supporting_text_snippet": "The MME receives an Attach Request from the UE."
    }},
    {{
      "type": "incorrect_edge_type",
      "edge": "Attach_Request_Received → UE_Attaching",
      "current_type": "condition",
      "suggested_type": "trigger",
      "description": "This event causes the transition, so it should be a 'trigger'."
    }},
    {{
      "type": "missing_transition",
      "from": "UE_Attaching",
      "event": "Auth_Challenge_Received",
      "to": "UE_Authenticating",
      "description": "Transition missing: UE receives auth challenge after attach.",
      "supporting_text_snippet": "The network initiates authentication once attach is processed."
    }},
    {{
      "type": "conflicting_node_type",
      "node": "Attach_Request",
      "current_types": ["state", "event"],
      "suggested_type": "event",
      "description": "Node is incorrectly labeled as both a state and an event."
    }},
    {{
      "type": "invalid_edge_reference",
      "edge": {{
        "from": "UE_Powered_On",
        "to": "Attach_Started"
      }},
      "description": "The node 'Attach_Started' does not exist in the node list."
    }},
  ]
}}

Flow Property Graph to Evaluate:
{json.dumps(extracted_data, indent=2)}

Original 3GPP Specification Section:
{original_content}


##Strict Rules##
Do not make assumptions or insert inferred behavior not grounded in the spec text.

Only judge against high-level control flow as intended in the extracted graph.

Return all relevant issues you find, no matter how small.

Maintain valid JSON structure for all responses.

Return ONLY the JSON object. 
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
