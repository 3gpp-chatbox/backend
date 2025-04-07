# Primary authentication and key agreement procedure - TXT file version
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_procedural_info_from_text(section_name, text):
    prompt = f""" Extract the full flow of the procedure {section_name} based on my provided context(i will put in the end of this message), ensuring the following: 

Capture main steps in sequence, including sub-steps and conditional actions.

Identify all involved entities (UE, AMF, SMF, timers, databases, etc.).

Extract NAS messages, specifying mandatory, optional, and conditional parameters.

Track implicit side effects triggered during the procedure (e.g., retries, service requests, timer expiration).

Ensure state dependencies (e.g., UE must be in Registered state before X action) are included.

Highlight policy-based modifications (e.g., roaming policies, DNN-specific behavior).

example Output Format(the content inside example is just example,mock info ): 
{{
  "procedure_name": "Initial Registration Procedure",
  "steps": [
    {{"id": 1, "step": "UE sends Initial Registration Request", "state_required": "Idle"}},
    {{"id": 2, "step": "AMF forwards request to SMF"}},
    {{"id": 3, "step": "AMF triggers Service Request if necessary"}}
  ],
  "entities": [
    {{"name": "UE", "role": "requester", "involved_steps": [1, 3]}},
    {{"name": "AMF", "role": "intermediary", "involved_steps": [2, 3]}}
  ],
  "messages": [
    {{
      "name": "Initial Registration Request",
      "from": "UE",
      "to": "AMF",
      "parameters": {{
        "mandatory": ["IMSI", "PLMN-Id"],
        "optional": ["MSISDN"],
        "conditional": {{"field": "Roaming-Indicator", "required_if": "Roaming condition met"}}
      }}
    }}
  ]
}}


My provided context: 

{text}"""

    response = model.generate_content(prompt).text.strip()
    return response

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