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
i will provide orginal sections context from 3gpp NAS specification that about procedure "{section_name},your task is :
1. Identify all the top-level conditions (list as a, b, c, d...). 
2. For each condition, note the operation (sending REGISTRATION REQUEST). 
3. Look for any sub-conditions within each main condition and represent them as branches in the graph. 
4. After the initial operation, identify any subsequent conditional steps and link them accordingly. 

return in below example json format:
{{
  "procedure": "Registration Procedure",
  "conditions": [
    {{
      "id": "a",
      "condition": "Initial Registration Request",
      "operation": "Send REGISTRATION REQUEST",
      "sub_conditions": [
        {{
          "id": "a1",
          "condition": "Network response received",
          "operation": "Wait for Network Response",
          "sub_conditions": [
            {{
              "id": "a1a",
              "condition": "Response received successfully",
              "operation": "Process RESPONSE",
              "sub_conditions": [
                {{
                  "id": "a1a1",
                  "condition": "Registration successful",
                  "operation": "Complete Registration"
                }},
                {{
                  "id": "a1a2",
                  "condition": "Registration failed",
                  "operation": "Send Registration Reject"
                }}
              ]
            }},
            {{
              "id": "a1b",
              "condition": "No response (timeout)",
              "operation": "Retry REGISTRATION REQUEST"
            }}
          ]
        }}
      ]
    }},
    {{
      "id": "b",
      "condition": "Registration Reject",
      "operation": "Handle REGISTRATION REJECT",
      "sub_conditions": [
        {{
          "id": "b1",
          "condition": "Reason for reject",
          "operation": "Analyze Reject Reason",
          "sub_conditions": [
            {{
              "id": "b1a",
              "condition": "Reject due to authentication failure",
              "operation": "Initiate Authentication Procedure"
            }},
            {{
              "id": "b1b",
              "condition": "Reject due to registration failure",
              "operation": "Retry Registration Procedure"
            }}
          ]
        }}
      ]
    }}
  ],
  "edges": [
    {{
      "from": "a",
      "to": "a1",
      "condition": "Network response received"
    }},
    {{
      "from": "a1",
      "to": "a1a",
      "condition": "Response received successfully"
    }},
    {{
      "from": "a1a",
      "to": "a1a1",
      "condition": "Registration successful"
    }},
    {{
      "from": "a1a",
      "to": "a1a2",
      "condition": "Registration failed"
    }},
    {{
      "from": "a1",
      "to": "a1b",
      "condition": "No response (timeout)"
    }},
    {{
      "from": "b",
      "to": "b1",
      "condition": "Registration Reject"
    }},
    {{
      "from": "b1",
      "to": "b1a",
      "condition": "Reject due to authentication failure"
    }},
    {{
      "from": "b1",
      "to": "b1b",
      "condition": "Reject due to registration failure"
    }}
  ]
}}


##this is provided sections context :
{text}

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
    save_procedural_info_to_json(procedural_info, "step1-condition.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1-condition.json")
else:
    print("Failed to clean json file")