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

I will provide excerpts from the 3GPP specification for the procedure "{section_name}". It contains the full section including subsections, titles, and section IDs.

Analyze the text and extract all events related to the procedure "{section_name}".

### Requirements:

1. defitnition of event:Triggers like messages received, timeouts, or failures.
2. Do NOT include hypothetical or inferred events. Use 3GPP domain knowledge only to help interpret terminology — not to invent content.
3. For each event, provide:
   - A unique numeric ID (sequential).
   - Event name (as exactly worded in the specification).
   - Metadata:
     - Clause(s) where the event is described (e.g., "5.1.3.6.5", which always starts with "#" in the text).
     - Direct quotes from the text describing or defining the event.

### Output format:

Respond with a **single valid JSON object only** in the format below. Do not include explanations, comments, or extra text.

Example output:
{{
  "procedure": {{
    "name": "{section_name}",
    "section_reference": "the section id",
    "events": [
      {{
        "id": 1,
        "name": "Registration Request received",
        "metadata": {{
          "section_reference": ["5.1.3.2"],
          "excerpts": [
            "Upon receipt of the Registration Request message, the AMF..."
          ]
        }}
      }},
      {{
        "id": 2,
        "name": "Authentication Failure",
        "metadata": {{
          "section_reference": ["5.1.3.4"],
          "excerpts": [
            "If authentication fails, the AMF shall..."
          ]
        }}
      }}
    ]
  }}
}}



Rely **only on the text** provided. However, you may use 3GPP domain knowledge **to interpret terminology or infer intent** — **but not to invent missing info**.

### Original document content 
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
    save_procedural_info_to_json(procedural_info, "step2-event.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step2-event.json")
else:
    print("Failed to clean json file")