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
You are an expert in 3GPP procedures, and you are tasked with creating a meta-procedure model for procedure "{section_name}".
I will provide key excerpts from 3GPP specification regarding procedure "{section_name}" in the end.

Based on that, define a meta‑procedure model that includes:
- The initial state,
- Triggers,
- Core operations,
- Conditional information elements (IEs),
- **Events**,
- Timers,
- Dependencies (e.g., security context and network slices),
- Variants.

Please develop a detailed taxonomy that includes the following elements:

- **Initial State:** What is the starting state of the UE before the procedure? (e.g., 5GMM-DEREGISTERED)

- **Triggers:** List all possible high-level reasons for starting the procedure, such as UE power-on, RAT change, emergency attach, etc.

- **Core Operation:** Describe the main goal of the procedure and the key message exchanges that define it.

- **Conditional Information Elements (IEs):** Identify IEs that may appear based on conditions such as security state or requested NSSAI.

- **Events:** Define all discrete, spec-relevant events that represent meaningful steps or transitions. For each event, include:
    - **Event Name**
    - **Triggering condition/message**
    - **Resulting action or state change**
    - **Involved timers, if any**
    - **Spec reference**
    - (Example: “T3510 expires → UE retransmits REGISTRATION REQUEST → State remains: WAITING_FOR_ACCEPT”)

- **Timers:** Note which timers are involved, when they start/stop, and what triggers timeout.

- **Dependencies:** Outline how the procedure depends on:
    - Security context (valid 5G NAS context, etc.)
    - Network slices (e.g., NSSAI)
    - Previous registration history or mode

- **Variants:** Identify variants such as emergency registration, onboarding via SNPN, SMS-only registration.

Organize the taxonomy in a tree-structured format and output in JSON like this:


example output format
{{
  "procedure": "Registration Initiation",
  "meta_model": {{
    "initial_state": {{
      "description": "UE starts in the 5GMM-DEREGISTERED state.",
      "reference": "TS 24.501, Section 5.5.1.2.2"
    }},
    "triggers": [
      {{
        "name": "Initial Registration Trigger",
        "conditions": [
          "UE performs initial registration for 5GS services",
          "UE performs initial registration for emergency services",
          "UE performs initial registration for SMS over NAS",
          "UE transitions from GERAN/UTRAN to NG-RAN coverage"
        ],
        "reference": "TS 24.501, Section 5.5.1.5.2"
      }}
    ],
    "core_operation": {{
      "action": "Send REGISTRATION REQUEST message to the AMF",
      "reference": "TS 24.501, Section 5.5.1.2.2"
    }},
    "conditional_IEs": [
      {{
        "IE": "5GS Mobile Identity IE",
        "conditions": [
          "Inclusion depends on whether a valid 5G NAS security context exists",
          "Mapping from valid 4G-GUTI if available"
        ],
        "reference": "TS 24.501, Section 5.5.1.2.2.1"
      }}
    ],
    "timers": [
      {{
        "timer": "T3510",
        "action": "Starts when REGISTRATION REQUEST is sent",
        "reference": "TS 24.501, Section 5.5.1.2.2"
      }},
      {{
        "timer": "T3502",
        "action": "Stopped if running when initiating registration",
        "reference": "TS 24.501, Section 5.5.1.2.2"
      }}
    ],
    "dependencies": {{
      "security_context": "Registration initiation must check if a valid 5G NAS security context is available.",
      "network_slices": "Include NSSAI information if supported/requested by the UE.",
      "previous_registration": "Reset or update registration attempt counter if previous registration exists."
    }},
    "variants": [
      "Emergency Registration",
      "SMS-only Registration",
      "Onboarding Registration (SNPN)"
    ]
  }}
}}



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
    save_procedural_info_to_json(procedural_info, "step1-meta.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1-meta.json")
else:
    print("Failed to clean json file")