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
You are a 3GPP procedure extraction tool. Using your knowledge of 3GPP procedures but based on the provided text,
 Extract the **decision logic, dependencies, and fallback conditions** for the procedure "{section_name}".do not make assumption.

### **Extraction Rules:**  
🔹 **For each decision point:**  
   1️⃣ Identify **the triggering condition** (explicitly stated in the spec).  
   2️⃣ Identify **all possible outcomes** (not just success/failure).  
   3️⃣ Identify **fallbacks caused by previous failures or timeouts**.  
   4️⃣ Identify **hidden dependencies** (e.g., Step 5 only occurs if Step 2 succeeded).  

🚀 **Output Format (Structured for Flow Property Graph):**  
{{
  "decision_points": [
    {{
      "step": Step number,
      "condition": "Main decision condition",
      "outcomes": [
        {{"outcome": "Success", "next_step": X}},
        {{"outcome": "Failure - Retry", "next_step": Y, "reason": "Timer expiry"}},
        {{"outcome": "Failure - Reject", "next_step": Z, "reason": "Authentication failure"}}
      ]
    }}
  ],
  "dependencies": [
    {{
      "step": X,
      "depends_on": Step Y,
      "type": "hard" or "conditional" or "retry",
      "reason": "Dependency explanation"
    }}
  ]
}}


Provided Context:
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
    save_procedural_info_to_json(procedural_info, "step2-v3.json")
else:
    print("Failed to extract procedural information")