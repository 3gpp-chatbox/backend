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
I will provide excerpts from the 3GPP specification for the procedure "{section_name}".  
Analyze the text and extract all states explicitly defined in the procedure.  

Requirements:  
1. Include only states directly named in the provided text (e.g., "5GMM-DEREGISTERED").  
2. For each state, provide:  
   - Unique numeric ID (sequential).  
   - Name (exact term from spec).  
   - Description (summarize the state’s meaning).  
   - Metadata:  
     - Spec clause(s) where the state is defined (e.g., "5.1.3.6.5").  
     - Direct quotes from the spec that define the state.  
     - Constraints (e.g., "UE must have valid 5G-GUTI").  

Format the output as JSON . Do not include hypothetical states.  
**Your entire response must ONLY be a single valid JSON object** in the following format. Do not include explanation, comments, or extra text.
Example output
{{
  "procedure": {{
    "name": "Initial Registration",
    "section_reference": "5.5.1",
    "states": [
      {{
        "id": 1,
        "name": "5GMM-DEREGISTERED",
        "description": "UE is not registered with the 5G network",
        "metadata": {{
          "ection_reference": ["5.1.3.4.2"],
          "excerpts": [
            "The UE shall be in the 5GMM-DEREGISTERED state when it is not registered for 5GS services."
          ],
          "constraints": [
            "UE must initiate registration before accessing services"
          ],
          "message_types": []  // Optional, if no messages are sent in this state
        }}
      }},
      {{
        "id": 2,
        "name": "5GMM-REGISTERED",
        "description": "UE is successfully registered with the network",
        "metadata": {{
          "section_reference": ["5.3.2.1"],
          "excerpts": [
            "The UE enters the 5GMM-REGISTERED state upon successful completion of the registration procedure."
          ],
          "constraints": [
            "UE must maintain periodic registration updates"
          ],
          "message_types": ["REGISTRATION ACCEPT"]
        }}
      }}
    ]
  }}
}}


Rely **only on the text** provided. However, you may use 3GPP domain knowledge **to interpret terminology or infer intent** — **but not to invent missing info**.

### PROCEDURE SECTION
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
    save_procedural_info_to_json(procedural_info, "step1-state.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1-state.json")
else:
    print("Failed to clean json file")