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
1. Original 3GPP specification text for section "{section_name}".
2. A proposed Flow Property Graph (FPG) for the procedure "{section_name}" in JSON format for the **UE side only**, containing both nodes and edges.

Your task is to **validate and correct** the FPG of the procedure "{section_name}" against the specification text, ensuring it accurately reflects only UE-side behavior and includes no inferred or incorrect content.

---

## Evaluation Tasks

###  For Nodes:
- Ensure each node is either a **UE-visible event** or an **explicitly named UE state**:
  - **States**: These are explicitly named states from the specification (e.g., "5GMM-DEREGISTERED", "5GMM-REGISTERED").
  - **Events**: These describe something that happens to the UE, such as "Receive REGISTRATION REJECT", "T3510 expires", or other triggers that affect the UE.
- Confirm that **events** describe something that happens **to** the UE (not something the UE performs). For example, an event like `"Receive REGISTRATION REJECT"` describes a message received **by the UE**.
- Confirm that **actions performed by the UE** (e.g., "Send REGISTRATION REQUEST", "Store context") are **not included** as nodes, as these are not events that happen **to** the UE.
- Ensure that **event nodes** are added only if they are mentioned as triggers in the edges but are missing in the node list (e.g., if the label "T3510 expires" appears in an edge but is not present as a node, add it as an event).

### For Edges:
- Validate that each edge connects valid nodes and represents a legitimate transition described in the text.
  - Accept the label if: It’s generally descriptive of the transition, it does not contradict the content, and it does not include inferred behavior.
  - The **label** must not contradict the content — *do not flag stylistic differences* or minor omissions. Only flag if **factually incorrect or misleading**.
- Check that the **section_reference** points to the correct part of the text justifying this transition.

---

## Correction Instructions

- **For valid nodes and edges**: Leave them unchanged.
- **For invalid nodes**:
  - If a node is invalid, **remove it** or **correct it** directly in the JSON structure.
  - If a valid event is mentioned in an edge but does not exist as a node, **add it** to the node list with a unique ID, ensuring it's properly categorized as an event (not an action).
- **For invalid edges**:
  - First, ensure that the **source and target nodes are valid**.
  - Then, validate the edge:
    - If the edge is invalid, **correct the edge** directly in the JSON structure.
- **If a node or edge is missing**:
  - Append it with a new unique ID (e.g., node13, edge9), placing it after the last listed item.
- Preserve original JSON formatting and structure in your output.

---

### Constraints:
- Do not make assumptions beyond the provided spec content.
- Focus only on UE-side behavior for procedure "{section_name}".
- Be conservative and grounded in exact wording — correctness comes from explicit evidence, not inference.

---

## Inputs

Provided Inputs:
-----------
Extracted Flow Property Graph:
{extracted_data}
-----------
Original sections content Provided:
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
    
    extracted_data = read_json_file("step1-v2.json")
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
    save_to_txt(procedural_info, "step2-validate-correct-v2.json")
else:
    print("Failed to evaluate")
