import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

load_dotenv()

flash_model = "gemini-1.5-flash"
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
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
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

def extract_procedural_info(section_name, extracted_data, originaltext):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
Using the following list of states and the original 3GPP spec text, extract all state-to-state transitions(no matter trigger by event or condition or both or what) that are described in the text for the procedure "{section_name}" on the UE side.
Each transition should include:
id
from (source state)
to (target state)
section_reference (e.g., "5.3.2.1.6.7")
brief description
do not make any assumption.all states are in the list.
Extract every transition, even if multiple go between the same pair of states,only extract for UE side.
only return json object,return in json Format as bellow:

[
  {{
    "from": "State1",
    "to": "State2",
    "transitions": [
      {{
        "id": "transition1",
        "section_reference": "5.3.2.1.6.7",
        "brief_description": "Description of the first transition from State A to State B."
      }},
      {{
        "id": "transition2",
        "section_reference": "5.3.2.1.6.8",
        "brief_description": "Description of the second transition from State A to State B."
      }}
    ]
  }},
  // ... more state pairs and their transitions

  ...
]

list of states:
{extracted_data}

original 3GPP spec text:
{originaltext}

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

def save_to_json(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")



def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    extracted_data = read_json_file("step1a-valicorrect-state.txt")
    originaltext = read_text_file("5.5.1.2.txt")

    if extracted_data is None or originaltext is None:
        print("Failed to load extracted_data or evaluation")
        return None

    procedural_info = extract_procedural_info(section_name, extracted_data, originaltext)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "step2-highlevel-transition.json")
else:
    print("Failed to correct")
