import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

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

def extract_procedural_info(section_name, extracted_data, original_content):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
Here is a list of extracted high-level transitions between states from the 3GPP procedure "{section_name}" on the UE side, along with the original text from the 3GPP spec.

Your task is to extract **detailed yet concise** information for these transitions between the states of the procedure "{section_name}" **ONLY on the UE side**.

For each transition, identify and extract the following information **step by step**, focusing on one destination state at a time. After extracting all transitions leading to that destination, move on to the next destination state.

When extracting, follow these strict rules:
- Base your findings **only on what is explicitly described in the original text** (no assumptions).
Summarize actions, events, and conditions clearly using standard protocol terminology (e.g., "send X", "start timer TXXXX", "delete Y", "retry Z", "if...", "when...", etc.).
- Do **not copy large paragraphs** of 3GPP text into the actions section—summarize and condense only the UE behavior.

---

Return your answer as a JSON object with the following format:

Example output:
{{
  "from_state": "UE_Attaching",
  "to_state": "Attach_Request_Received",
  "transitions": [
    {{
      "id": "transition1",
      "event(s)": [
        "Attach Request message is received"
      ],
      "conditions": [
        "UE is in IDLE mode",
        "PLMN is allowed"
      ],
      "actions": [
        "start timer T3410",
        "send Attach Complete",
        "set EPS update status to 'updated'"
      ],
      "section_reference": "5.5.2.4.5"
    }}
    ...more transition if applicable
  ]
}}


list of extracted high level transitions:
{extracted_data}

original text provided:
{original_content}

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

def save_to_txt(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")



def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    extracted_data = read_json_file("step2-highlevel-transition.json")
    original_content = read_text_file("5.5.1.2.txt")

    if extracted_data is None or original_content is None:
        print("Failed to load extracted_data or original_content")
        return None

    procedural_info = extract_procedural_info(section_name, extracted_data, original_content)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_txt(procedural_info, "step3-detail-transition.json")
else:
    print("Failed to evaluate")
