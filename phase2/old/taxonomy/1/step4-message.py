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
Analyze the 3GPP specification text below to extract protocol metadata with technical precision.
Focus on procedure - {section_name}.

Requirements:
1. Message Types:
   - Identify NAS/RRC message types (e.g., REGISTRATION REQUEST)
   - Classify directionality: UE->Network or Network->UE
   - Identify mandatory/optional IEs

2. Constraints:
   - UE requirements (capabilities/configurations)
   - Network requirements (supported features)
   - Security context dependencies
   - Inter-procedure dependencies

3. Related Procedures:
   - Directly referenced subsequent procedures
   - Contingency procedures
   - Conflicting procedures

Formatting Rules:
- Use 3GPP message naming exactly as in specs
- Include spec clause references for every element
- Maintain original constraint wording
- Flag implicit relationships with [INFERRED]

Output Template:
{{
  "metadata": {{
    "message_types": [
      {{
        "id": "MSG_001",
        "name": "REGISTRATION REQUEST",
        "direction": "UE->AMF",
        "ies": {{
          "mandatory": ["5G-GUTI", "SUCI"],
          "optional": ["Requested NSSAI"]
        }},
        "clauses": ["5.5.1.2.2"],
        "excerpts": [
          "The UE shall include 5G-GUTI if available..."
        ]
      }}
    ],
    "constraints": [
      {{
        "id": "CON_001",
        "type": "security_context",
        "description": "Valid 5G NAS security context required for NAS container IE",
        "scope": "UE",
        "clauses": ["5.5.1.2.2 Note 3"]
      }}
    ],
    "related_procedures": [
      {{
        "id": "REL_001",
        "name": "Deregistration",
        "relationship": "subsequent",
        "clauses": ["5.5.1.3.2"],
        "trigger_condition": "On registration failure"
      }}
    ]
  }}
}}

Validation Rules:
1. Every message type must have ≥1 associated IE
2. Constraints must specify UE/Network scope
3. Procedural relationships require clause references

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
    save_procedural_info_to_json(procedural_info, "step4-message.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step4-message.json")
else:
    print("Failed to clean json file")