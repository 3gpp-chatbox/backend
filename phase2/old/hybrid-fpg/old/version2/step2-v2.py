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
    prompt = f"""
You are a 3GPP specification expert. Analyze the decision points, fallback conditions, and dependencies in the procedure "{section_name}" from the provided context.

Identify:

-   Conditions that cause the procedure to branch or take different paths.
-   Timers that trigger fallbacks or retries.
-   Dependencies between steps (which steps must happen before others).
-   Any state transitions that depend on conditions (e.g., errors, timeouts).
-   The step number that the decision point or dependency is related to.

example Output the information in the following JSON format:

{{
  "decision_points": [
    {{"step": Step number, "condition": "Description of the condition and its outcome"}},
    // ... more decision points ...
  ],
  "dependencies": [
    {{"step": Step number, "depends_on": Step number, "type": "hard" or "conditional" or "retry", "condition": "Condition (if applicable)"}},
    // ... more dependencies ...
  ]
}}

Provided Context:
{text}
"""

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
    save_procedural_info_to_json(procedural_info, "step2-v2.json")
else:
    print("Failed to extract procedural information")