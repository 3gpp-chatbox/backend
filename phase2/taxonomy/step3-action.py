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
Analyze the provided 3GPP specification text for the "{section_name}" procedure. 
Extract all procedural actions and their associated error handling mechanisms with technical precision.

Requirements:
1. Identify actions using 3GPP normative language ("shall", "must"):
   - Message transmission (NAS/RRC)
   - Timer operations (start/stop)
   - Security context management
   - State transitions
2. For each action, extract:
   - `id`: Sequential numeric ID starting at 1
   - `action_type`: Technical category from:
     [registration_request, authentication, timer_management, security_activation, state_transition]
   - `description`: Concise 5GMM/NAS technical summary
   - `error_handling`: {{
       "type": [timer_expiry|retry_limit|security_failure],
       "response": Specific recovery action,
       "clause": Spec reference
     }}
   - `metadata`: {{
       "clauses": [List of spec clauses],
       "excerpts": [Verbatim text snippets],
       "ies": [Information Elements involved]
     }}

Rules:
- Maintain 3GPP terminology exactly (e.g., "5GMM-DEREGISTERED", "T3510")
- Only include actions explicitly described
- Prioritize machine-readability over natural language

JSON Output Template:
{{
  "procedure": {{
    "name": "{section_name}",
    "technical_reference": "24.501",
    "actions": [
      {{
        "id": 1,
        "action_type": "registration_request",
        "description": "UE transmits REGISTRATION REQUEST message",
        "error_handling": {{
          "type": "timer_expiry",
          "response": "Retry procedure after T3510 timeout",
          "clause": "5.5.1.2.3"
        }},
        "metadata": {{
          "clauses": ["5.5.1.2.2"],
          "excerpts": [
            "The UE shall send a REGISTRATION REQUEST message containing 5G-GUTI..."
          ],
          "ies": ["5G-GUTI", "SUCI"]
        }}
      }}
      //more actions..
    ]
  }}
}}

Specification Text:
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
    save_procedural_info_to_json(procedural_info, "step3-action.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step3-action.json")
else:
    print("Failed to clean json file")