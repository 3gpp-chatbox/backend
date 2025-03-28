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
    prompt = f""" Analyze the decision points, fallback conditions, and dependencies in the procedure" {section_name}" based on my provided context(i will put in the end of this message), ensuring the following: 

Identify state-based decision nodes (e.g., retry logic, error handling).

Extract timer-driven fallbacks and recovery paths.

Map dependencies between steps (hard, soft, retry loops).

Specify conditional state transitions (e.g., authentication failure leads to re-authentication).

example Output Format(the content inside example is just example,mock info ): 
{{
  "decision_points": [
    {{"step": 4, "condition": "If registration fails, trigger retry"}},
    {{
      "step": 5,
      "condition": {{
        "if": "Authentication fails",
        "then": "Request re-authentication",
        "else": "Proceed to step 6",
        "timeout": "Trigger Timer T3510 if no response within 5 seconds"
      }}
    }}
  ],
  "dependencies": [
    {{"step": 2, "depends_on": 1, "type": "hard"}},
    {{"step": 3, "depends_on": 4, "type": "conditional", "condition": "if Step 4 succeeds"}},
    {{"step": 5, "loop_on": 4, "type": "retry", "condition": "Retry if no response within 3 attempts"}}
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
    save_procedural_info_to_json(procedural_info, "step2.json")
else:
    print("Failed to extract procedural information")