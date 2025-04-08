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

 You are given two part. first part is an extracted state machine (in JSON format) for the  procedure "{section_name}", 
 second part is  original specification document.
 Compare the extracted info(first part) with the official specification(second part) to identify missing or incorrect elements.

Calculate a coverage score for each category based on the percentage of the expected elements that are present:
Core Path Accuracy (e.g., states, transitions)
Timer Accuracy (e.g., timers, values)
State Transitions and Actions (e.g., correct actions at each state)
Error Handling and Special Cases (e.g., failures, re-transmissions)
The coverage score for each category will be calculated as:

Coverage Score=(Number of Correct Elements/Total Number of Expected Elements)×100

Then, compute a weighted final score by assigning weight to each category based on the importance of each procedure component. Here is the structure:
Core Path Accuracy: [Weight: 30%]
Timer Accuracy: [Weight: 20%]
State Transitions and Actions: [Weight: 25%]
Error Handling and Special Cases: [Weight: 25%]
Steps:
Identify the expected elements in each category from the [Specification Name] specification.
Compare them with the elements in the extracted JSON graph.
Calculate the percentage of correct elements in each category.
Compute a final score for each category.
Compute the total score by applying the weights for each category.
Report the results with a clear breakdown of coverage percentages and scores for each category.
If any element is missing or incorrect, deduct from the total score accordingly based on the severity of the missing part.
Example of Extracted Data (Input JSON):
{{
  "CorePath": ["State1 → Transition1", "Transition2", "Transition3", "State2"],
  "Timers": ["Timer1", "Timer2"],
  "States": ["State1", "State2"],
  "Actions": ["Action1", "Action2"]
}}

Output Format:
Core Path Accuracy:
Expected: 10 transitions
Found: 5 transitions
Coverage: 50%
Weighted Score: 50 × 0.30 = 15

Timer Accuracy:
Expected: 3 timers
Found: 2 timers
Coverage: 66.67%
Weighted Score: 66.67 × 0.20 = 13.33

State Transitions and Actions:
Expected: 8 transitions/actions
Found: 4 transitions/actions
Coverage: 50%
Weighted Score: 50 × 0.25 = 12.5
Error Handling and Special Cases:
Expected: 3 error handling cases
Found: 1 error handling case
Coverage: 33.33%
Weighted Score: 33.33 × 0.25 = 8.33
Total Score:
(15 + 13.33 + 12.5 + 8.33) = 49.16 (out of 100)

Key Points:
Comparing Elements: This is the core of the prompt. You need to define the expected elements for each category (states, transitions, timers, actions, etc.) based on the relevant specification for the procedure you're analyzing. This can be done by referring to documents like the 3GPP TS, RFCs, or other procedure standards.
Calculating Coverage: For each category, you will calculate how much of the expected elements are present in the extracted data (e.g., compare the transitions or actions in the JSON data with those listed in the specification).
Scoring Based on Coverage: The percentage of correct elements in each category determines the coverage score. This score is then multiplied by the category's weight to calculate the weighted score.
Final Total Score: The final score represents the overall accuracy of the extracted procedure against the specification, considering all the categories and their respective weights.
**Strict Rule**: Use **only** the provided text. Do **not** infer or add missing details.  

This is first part.(extracted flow property graph of procedure in json format)
{json.dumps(extracted_data, indent=2)}

------------------
This is second part:
#### **orginal content from 3gpp specification:**  
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
    
    extracted_data = read_json_file("v06-step3-complex-flashmodel.json")
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
    save_to_txt(procedural_info, "v06-evaluation-byflashmodel.txt")
else:
    print("Failed to evaluate")
