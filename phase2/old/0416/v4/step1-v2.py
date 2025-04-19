# Primary authentication and key agreement procedure - TXT file version
import os
from dotenv import load_dotenv
from google import genai
import json

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


def extract_procedural_info_from_text(section_name, text):
    prompt = f"""
    
I will provide you with the original content of sections of the 3GPP specification related to procedure "{section_name}".

I want you to extract the flow property graph for this procedure "{section_name}" only on the UE side and return it as a JSON object in the format specified below.

Core Components to Identify (remember only extract on UE side):

□ States: Different conditions or statuses of the UE (e.g., 5GMM-DEREGISTERED, 5GMM-REGISTERED). Extract only explicitly named states.
□ Actions: Operations performed by the UE during a transition.
□ Events: Triggers that cause transitions between states (e.g., receiving a message, a timer expiring, an internal decision).
□ Parameters: Data exchanged or required during the procedure (list them within the 'properties' of nodes and edges).
□ Flow of Execution: The sequence of steps and transitions in the procedure.
□ Conditionals: Criteria that determine which transition occurs (describe these in the 'condition' property of edges).
□ Metadata: Additional relevant information like message types, timer names, or identifiers (include within the 'properties' of nodes and edges).
□ Section Reference: The specific section id in the 3GPP specification where the information is found (include in the 'properties' of edges).

Step 1: Identify and extract Key Steps and elements on the UE side of the procedure described in the provided text.

Step 2: Represent the Model as a Flow Property Graph:
Nodes represent States and Events.
Edges represent Actions and Transitions, capturing the Flow of Execution.
Properties within nodes and edges will include Parameters, Conditionals, Metadata, and Section Reference.

Step 3: Structure the JSON Output as follows:

{{
  "nodes": [
    {{
      "id": "node1",
      "name": "StateOrEventName",
      "type": "state" or "event",
      "properties": {{
        "description": "Brief description from the text (if available)",
        "parameter1": "value1",
        "metadata_key": "metadata_value"
      }},
      "parameters": ["list", "of", "parameters", "relevant", "to", "this", "node"] (only for event nodes if clearly listed)
    }},
    {{
      "id": "node2",
      "name": "AnotherStateOrEvent",
      "type": "state" or "event",
      "properties": {{...}},
      "parameters": [...]
    }},
    ...
  ],
  "edges": [
    {{
    "id": "edge1",
      "from": "source_node_id",
      "to": "target_node_id",
      "action": "UE_Action_Performed",
      "properties": {{
        "parameters": ["list", "of", "parameters", "exchanged/used"],
        "condition": "Condition that triggers this transition (if any)",
        "metadata": {{
          "message_type": "MessageType (if applicable)",
          "timer_started": "TimerName (if started)",
          "timer_stopped": "TimerName (if stopped)"
        }},
        "section_reference": "5.2.4.2.1.4"
      }}
    }},
 
    ...
  ]
}}

Constraints for Extraction:

* **UE Side Only:** Focus solely on the UE's behavior, states, actions, and events. Ignore network-side operations unless they directly trigger a UE event (e.g., receiving a message).
* **Explicit States:** Only extract states that are explicitly named as states in the 3GPP text (e.g., "5GMM-REGISTERED").
* **Condition vs. Action:** For edges, the 'condition' property should describe what *triggers* the transition. The 'action' property should describe the operation the UE *performs* during the transition.
* **Include Section Reference:** For every edge, include the 'section_reference' indicating where this flow is described in the provided text.
* **Consistent Edge Properties:** For all edges where applicable based on the 3GPP text, include 'parameters', 'condition', and 'section_reference' within the 'properties'. If no specific value is mentioned, use 'None' or an empty list/object as appropriate.
* **Timer Events:** Explicitly identify timer expiry as 'event' nodes and show the transitions they trigger from the state where the timer is active. Include the timer name in the event node's properties.

Only return the JSON object. Do not include any introductory or explanatory text.

----
This is the original content, only analyze based on my provided text, do not make assumptions:

{text}
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

def save_procedural_info_to_json(procedural_info, file_path):
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(procedural_info)
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

def process_text_file(input_file_path, section_name):
    """Processes content from a text file instead of database."""
    text_content = read_text_file(input_file_path)
    if text_content is None:
        return None
        
    procedural_info = extract_procedural_info_from_text(section_name, text_content)
    return procedural_info

# Example usage: Processing a text file
input_file_path = "5.5.1.2.txt"  # Path to your input text file
section_name = "Registration procedure for initial registration"  # Name of the section/procedure

procedural_info = process_text_file(input_file_path, section_name)

if procedural_info:
    save_procedural_info_to_json(procedural_info, "step1-v2.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1-v2.json")
else:
    print("Failed to clean json file")