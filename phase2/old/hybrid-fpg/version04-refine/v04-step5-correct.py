import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

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





def read_json_file(file_path):
    """Reads content from a JSON file and returns the parsed JSON object."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in {file_path}")
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

def extract_procedural_info(section_name, extracted_data, evaluation):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""
I will provide you with two parts:

1. **First part**: My extracted procedure flow property graph information for the 3GPP procedure "Registration procedure for initial registration."
2. **Second part**: An AI evaluation comparing my extracted data to the original content of "Registration procedure for initial registration" from the 3GPP NAS specification.

Please use the second part (the AI evaluation) to correct the first part (my extracted data) and return the corrected JSON.

**Strict Rule**: Use **only** the provided text. Do **not** infer or add missing details.

Let’s begin.

#### **Extracted procedure flow property graph info:**  

{json.dumps(extracted_data, indent=2)}

------------------
#### **AI Evaluation:**  
{evaluation}

After evaluation, please:
- Correct the first part (my extracted data) and return the corrected JSON.
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
    
    extracted_data = read_json_file("v04-step3-simple-flashmodel.json")
    evaluation = read_text_file("v04-step4-evaluation.txt")

    if extracted_data is None or evaluation is None:
        print("Failed to load extracted_data or evaluation")
        return None

    procedural_info = extract_procedural_info(section_name, extracted_data, evaluation)
    return procedural_info

# Example usage: Processing the procedure with step1.json and step2.json
section_name = "Registration procedure for initial registration"

procedural_info = process_procedure(section_name)

if procedural_info:
    save_to_json(procedural_info, "v04-step5-correct.json")
else:
    print("Failed to extract procedural information")
