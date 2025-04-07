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
You are a 3GPP procedure analysis expert, your task is to extract flow property graph of procedure " {section_name}".

From my provided text (sections context), extract the following components **while preserving their context**:

- **States**: System or UE conditions (e.g., UE_Powered_On, UE_Attaching)
- **Events**: Discrete incidents or message receptions (e.g., Attach_Request_Received)
- **Actions**: Activities performed by network functions or UE (e.g., Send_Attach_Request)

**Strict Rule**: 
When identifying information, you may rely on your pretrained knowledge of 3GPP procedures to understand terms like states, events, and actions if they are not explicitly defined in the provided content.
When extracting information, you must rely solely on the provided content .
Do not make assumptions, and do not introduce information beyond the provided text.



Provide the results in this format, ensuring you preserve any context and relationships between the states, events, and actions:

example output format:
{{
  "states": [
    {{"state_name": "UE_Powered_On",}},
    {{"state_name": "UE_Attaching"}},
    ...
  ],
  "events": [
    {{"event_name": "Attach_Request_Received", "trigger": "Attach Request message received from UE"}},
    {{"event_name": "Authentication_Challenge", "trigger": "UE sends authentication challenge"}},
    ...
  ],
  "actions": [
    {{"action_name": "Send_Attach_Request", "state_change": "UE_Powered_On → UE_Attaching"}},
    {{"action_name": "Initiate_Authentication", "state_change": "UE_Attaching → UE_Authenticating"}},
    ...
  ]
}}

### my provided sections context ###
 {text}

**Strict Rule**: 
When identifying information, you may rely on your pretrained knowledge of 3GPP procedures to understand terms like states, events, and actions if they are not explicitly defined in the provided content.
When extracting information, you must rely solely on the provided content 
Do not make assumptions, and do not introduce information beyond the provided text.

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
    save_procedural_info_to_json(procedural_info, "v1-step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("v1-step1.json")
else:
    print("Failed to clean json file")