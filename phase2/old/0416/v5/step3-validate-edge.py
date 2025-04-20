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
flash_20 = "gemini-2.0-flash"

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

You are provided with:
1. Original text from the 3GPP specification regarding the procedure "{section_name}".
2. several edges of the Flow Property Graph (FPG) for procedure "{section_name}" on the UE side in JSON format, previously extracted using a structured methodology.

Your task is to **evaluate the accuracy and completeness of the EDGE info only** in the provided edges, focusing solely on **UE-side** behavior.

---

## Evaluation Objectives

For each edge in the FPG:
-  Validate that the **source and target nodes** are correct according to the provided spec text.
-  Ensure that the **action(s)** listed are **explicitly described** or clearly implied in the text — do not infer actions that are not mentioned.
-  Check that all **conditions** are accurate and extracted **exactly as written** (if paraphrased, they must be faithful to the original meaning).
-  Ensure that **contextual dependencies** (e.g., security context, flags, counters) are correctly included when relevant.
-  Confirm that the **section_reference** matches the part of the original text justifying the edge.
-  Identify **invalid edges** or **extra transitions** that are not supported by the input. You do not need to identify missing edges, as the provided edges are only a subset.

---

## Evaluation Output Format

For each edge, return the following format:

```json
{{
  "incorrect_edges": [
    {{
      "edge_id": "edge1",
      "issues": [
        "Issue 1: Description of the problem with the edge.",
        "Issue 2: Another issue related to the edge."
      ],
      "suggested_correction": "Suggested changes to fix the issues, such as correcting the 'action' field to 'Send REGISTRATION ACCEPT'. and so on if application"
    }}
  ],
  "correct_edges": [
    "edge10",
    "edge8",
    "edge7"
  ]
}}

Constraints
Do not make assumptions outside of the provided text.
Focus only on the edges section of the FPG.
Your evaluation must be grounded in the exact wording and intent of the 3GPP original content.

Provided Inputs
-----------
Extracted edges subeset of Flow Property Graph:
{extracted_data}
-----------

Original sections content Provided:
{original_content}
"""




    model_to_use = flash_20  # or pro_model depending on your requirement
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
    
    extracted_data = read_json_file("edges_batch_1.json")
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
    save_to_txt(procedural_info, "correct_edges_bacth_1.json")
else:
    print("Failed to evaluate")
