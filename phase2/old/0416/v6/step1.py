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
You will be provided with original content from 3GPP specification sections describing the procedure: "{section_name}".

Your task is to extract the **Flow Property Graph (FPG)** for this procedure **on the UE side only**, and represent it as a structured JSON object following the format defined below.

**Do not infer or assume any information beyond what is explicitly stated in the provided text.** Focus on accurate and traceable extraction of clearly described elements.

---

## Objectives

Build a flow property graph where:
- **Nodes** are UE states or events (e.g., timer expiry, message reception).
- **Edges** represent transitions triggered by events, showing **explicit** actions the UE performs.
- The graph must include metadata, conditions, parameters, and context **only if they are explicitly stated**.

---

## Core Components to Extract (UE Side Only)

- **States**: Only explicitly named UE states from the spec (e.g., `"5GMM-DEREGISTERED"`).
- **Events**: UE-visible triggers like timer expiries or received messages (e.g., `"Receive REGISTRATION ACCEPT"`, `"T3510 expires"`).
- **Actions**: Only include UE-side actions that are **explicitly described** in the text.
- **Conditions**: Include **only** conditions that are clearly stated and affect the transition path.
- **Parameters**: Counters, flags, identifiers, or values explicitly mentioned (e.g., `registration_attempt_counter`).
- **Contextual Dependencies**: Clearly described inputs affecting the UE’s behavior (e.g., “if a valid security context exists”).
- **Fallbacks & Error Paths**: Include explicitly described rejections, failures, and timeout behavior.
- **Cause Values**: If cause values or reason codes are given, include them.
- **Section Reference**: Every edge must include the 3GPP section number from which it is derived.

---

## JSON Output Format

```json
{{
  "nodes": [
    {{
      "id": "node1", // unique node ID
      "name": "StateOrEventName",
      "type": "state" or "event",
      "properties": {{
        "description": "Short summary if explicitly stated",
        "cause_value": "optional"
      }},
      "parameters": ["T3510", "registration_attempt_counter"]  // Only if explicitly mentioned
    }}
    ...
  ],
  "edges": [
    {{
      "id": "edge1", // unique edge ID
      "from": "source_node_name",
      "to": "target_node_name",
      "action": [
        "Send REGISTRATION REQUEST"
      ],
      "condition": [
        "T3510 expired",
        "registration_attempt_counter = 5"
      ],
      "properties": {{
        "parameters": ["registration_attempt_counter"],
        "context": {{
          "security_context": "valid"
        }},
        "section_reference": "e.g. 5.5.1.3.2"
      }}
    }}
    ...
  ]
}}
Constraints & Guidance
UE Side Only: Do not include network-side states or actions unless they directly trigger UE behavior.
No Inference: This task focuses on extracting only what is explicitly stated. Do not include implied or inferred logic.
Clean Separation: Avoid mixing inferred logic with extracted facts. This allows engineers to verify core logic before expanding with implied details in a future phase.
Consistent Structure: Use fields like context, parameters, and section_reference consistently across all entries.
Explicit States Only: Do not invent or infer states — only use states explicitly defined in the text (e.g., “5GMM-REGISTERED”).
Multiple Paths: Include all explicitly described variants (e.g., emergency mode, valid/invalid security context).
Condition vs. Action: Keep conditions (triggers) separate from actions (UE responses).
Timer Events: Model timer expiries as their own event nodes, not embedded within edge conditions.
Contextual Inputs: If the UE uses flags, counters, or remembered values (and they are mentioned), extract them as context.
Fallbacks: Capture all valid fallback/error/rejection flows if explicitly described.

Only Use Provided Text: Do not reference or rely on external knowledge. Work solely from the provided content.

Input Below
This is the original content. Only analyze based on this input. Do not make assumptions:
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