# Primary authentication and key agreement procedure - TXT file version
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



def extract_procedural_info_from_text(section_name, text):
    prompt = f"""
You are a 3GPP procedure extraction tool. Using your knowledge of 3GPP procedures, but strictly based on the provided text, extract the high-level flow and key properties of the procedure "{section_name}".

## ** What to Extract (Fixed Scope)**

Extract the following **essential elements** while preserving the **cause-effect structure**:

 **Steps**:  
- Actions performed by the **UE, AMF, or other entities**.  
 **Messages**:  
- Key NAS messages exchanged (e.g., **REGISTRATION REQUEST, REGISTRATION ACCEPT**).  
 **State Transitions**:  
- **UE state changes** (e.g., `5GMM-DEREGISTERED → 5GMM-REGISTERED`).  
- If the state transition is **unclear or ambiguous**, flag it instead of omitting it.  
 **Timers**:  
- **Important timers started or stopped** (e.g., `T3519, T3550`).  
- **Explicit conditions for timer start/stop** must be extracted.  
 **Entities**:  
- The **entity performing each step** (`UE, AMF`, etc.).  

 ## ** Strict Rules**
 **Do NOT** make assumptions or infer missing details.  
 **Only extract what is explicitly stated** in the provided text.  
 **Ensure timers and state transitions are linked** to their triggering steps.  
 **Verify extracted steps follow logical order** (e.g., no missing preconditions).  
 **Flag inconsistencies instead of omitting unclear dependencies.** 

How to Extract (Refinable Method)
### ** 1. Ensure Complete State Transitions**
- **Extract full state transitions if explicitly stated.**  
- If **part of a transition is unclear**, flag it with `"note": "Potential missing transition dependency"`.
### ** 2. Maintain Logical Order**
- **Ensure extracted steps follow a valid sequence** based on **cause-effect relationships**.  
- If a step **implicitly requires another step** (e.g., **a timer must expire before retrying a message**), link them **even if the text does not explicitly say so**.
### ** 3. Explicitly Link Timers to Conditions**
- **Clearly extract when a timer starts or stops**.  
- If a **timer's trigger condition is missing**, flag it with `"note": "Possible missing condition"` instead of making assumptions.

---


 Output the information in the following example JSON format:


{{
  "procedure_name": "{section_name}",
  "steps": [
    {{
      "id": 1,
      "step": "Description of the first main step",
      "state_before": "Initial UE state(if applicable)",
      "state_after": "Resulting state (if applicable)",
      "entity": "UE or AMF",
      "note": "Any ambiguity in the state transition"
    }},
    {{
      "id": 2,
      "step": "Description of  the next main step",
      
      "entity": "UE or AMF"
       "note": "Any ordering dependency or missing link"
    }},
    // ... more steps ...
  ],
  "messages": [
    {{
      "name": "Message name",
      "from": "UE or AMF",
      "to": "UE or AMF"
    }},
    // ... more messages ...
  ],
  "timers": [
    {{
      "name": "Timer name",
      "action": "start or stop",
      "step_id": 1,
       "conditions": "Explicit condition under which the timer starts or stops"
        "note": "If any condition dependency is unclear"
    }},
    // ... more timers ...
  ]
}}

Provided Context:
{text}
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
    save_procedural_info_to_json(procedural_info, "v06-step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("v06-step1.json")
else:
    print("Failed to clean json file")
