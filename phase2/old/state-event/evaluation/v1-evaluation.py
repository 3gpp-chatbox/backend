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

def extract_procedural_info(section_name, extracted_data, original_content):
    """Generates a structured **flow property graph** using data from step1.json and step2.json"""
    
    prompt = f"""

You are a 3GPP procedure analysis expert and evaluator.

You are given:
1. An **extracted flow property graph** (state-event model) for 3GPP procedure "{section_name}".
2. The **original specification content** from which this graph was extracted.

Your task is to **evaluate** the quality of the extracted graph by comparing it to the original specification content using the following professional evaluation dimensions:

---

### 🔍 Evaluation Dimensions

1. **Structural Accuracy (0–10)**  
   - Are states and events clearly and correctly differentiated?  
   - Are edge types valid (e.g., 'trigger', 'condition') and correctly used?

2. **Semantic Correctness (0–10)**  
   - Do the states, events, and transitions match the meanings and intent of the original specification?  
   - Are transitions logically correct?

3. **Coverage (0–10)**  
   - Are all major states and events from the procedure represented?  
   - Are important transitions captured?

4. **Faithfulness to Source (0–10)**  
   - Is all content derived strictly from the specification (no hallucinated nodes or transitions)?  
   - Are naming and ordering consistent with the spec?

---

Please return your evaluation in the following format:

```json
{{
  "procedure_name": "Name of the Procedure",
  "scores": {{
    "structural_accuracy": <score from 0 to 10>,
    "semantic_correctness": <score from 0 to 10>,
    "coverage": <score from 0 to 10>,
    "faithfulness": <score from 0 to 10>
  }}
,
  "comments": {{
    "structural_accuracy": "Comment about structure here...",
    "semantic_correctness": "Comment about semantic alignment here...",
    "coverage": "Comment about completeness here...",
    "faithfulness": "Comment about whether graph sticks to spec..."
  }}

}}


Flow Property Graph JSON (extracted):
{json.dumps(extracted_data, indent=2)}

------------------

#### **orginal content from 3gpp specification:**  
{original_content}

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

def save_to_txt(data, file_path):
    """Saves procedural info to a JSON file."""
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data)
    print(f"Procedural info saved to {file_path}")



def process_procedure(section_name):
    """Processes the procedure using step1.json and step2.json as input."""
    
    extracted_data = read_json_file("v1-step2.json")
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
    save_to_txt(procedural_info, "v1-evaluation.txt")
else:
    print("Failed to evaluate")
