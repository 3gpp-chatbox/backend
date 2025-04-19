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

I will provide you with the original content of sections of the 3GPP specification related to the procedure "{section_name}".

Your task is to extract the **Flow Property Graph** for this procedure "{section_name}" **only on the UE side** and return it as a structured **JSON object** in the format described below.
should not assume any knowledge (beyond what's provided) when describing nodes and edges
---

##  Objectives

Extract and represent the procedure as a flow property graph where:
- **Nodes** are UE states or events (e.g., timer expiry, message reception).
- **Edges** are transitions triggered by events, showing actions performed by the UE.
- The structure includes metadata, conditions, parameters, and contextual dependencies.

---

##  Core Components to Identify (UE Side Only)

□ **States**: Explicit UE states (e.g., 5GMM-DEREGISTERED, 5GMM-REGISTERED).

□ **Events**: Triggers like timer expiry, message reception, internal decisions (e.g., "T3510 expires", "Receive AUTHENTICATION REQUEST").

□ **Actions**: Operations performed by the UE during transitions (e.g., "Start T3502", "Send REGISTRATION REQUEST").

□ **Parameters**: Counters, flags, IDs, or fields mentioned (e.g., registration_attempt_counter).

□ **Conditionals**: Conditions determining path selection (e.g., "if no valid security context", "attempts < 5").

□ **Contextual Dependencies**: UE-side inputs that affect behavior (e.g., existing security context, registered slices, attempt counters, configuration).

□ **Variants**: Alternative flows based on emergency mode, PDU sessions, rejected slices, etc.

□ **Cause Values / Reason Codes**: If mentioned, include in conditions or as `cause_value`.

□ **Fallbacks / Abort Paths**: Include UE responses to rejection, failure, or timeout.

□ **Section Reference**: Every transition (edge) must include the relevant 3GPP section.

---

##  JSON Output Format

```json
{{
  "nodes": [
    {{
      "id": "node1" // unique ID per node, after would be node2, node3,...
      "name": "StateOrEventName",
      "type": "state" or "event",
      "properties": {{
        "description": "Optional short summary from the text",
        "metadata_key": "metadata_value",
        "cause_value": "optional"
      }},
      "parameters": ["list", "of", "parameters"]  // Only for event nodes if explicitly given
    }},
    {{
  "id": "node2",
  "name": "T3510 expiry",
  "type": "event",
  "properties": {{
    "description": "Indicates T3510 timer expired",
    "cause_value": "15"
}},
  "parameters": ["T3510"]
}}

    ...
  ],
  "edges": [
    {{
      "id": "edge1"// unique ID per edge
      "from": "source_node_name",
      "to": "target_node_name",
      "action": [
        "Start T3502 (if value > 0)",
        "Stop T3510",
        "Send Registration Request"
      ],
       "condition": 
       ["Lower layer failure occurred",
        " registration_attempt_counter = 5",
         " Not emergency registration"
         ],
      "properties": {{
        "parameters": ["registration_attempt_counter", "emergency_service_flag"]
        "context": {{
          "security_context": "valid/invalid",
          "slice_requested": "yes/no"
        }},
        "metadata": {{
          "message_type": "REGISTRATION REQUEST"
        }},
        "section_reference": "e.g. 5.5.1.2.3"
      }}
    }},
    ...
  ]
}}
 Constraints & Guidance
UE Side Only: Do not include network states or actions unless they directly trigger UE-side behavior.
Explicit States: Only include named states from 3GPP (e.g., “5GMM-REGISTERED”), not inferred ones.
Multiple Paths: Capture all variants if alternative flows are described (e.g., emergency registration, valid security context).
Condition vs. Action: Clearly distinguish what triggers (condition) from what UE does (action).
Timer Events: Model timer expiries as separate event nodes, not just implicit in edges.
Contextual Info: Extract any described UE-side inputs (e.g., flags, counters, memory of last message) into context.
Fallbacks: Include all error paths (rejections, failures, timeouts) as valid branches.
---
Only Use Provided Text: Do not assume or add external knowledge — extract only from provided content.
 Input Below
This is the original content, only analyze based on my provided text. Do not make assumptions:
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
    save_procedural_info_to_json(procedural_info, "step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1.json")
else:
    print("Failed to clean json file")