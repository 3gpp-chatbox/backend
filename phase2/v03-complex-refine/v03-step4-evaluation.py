import os
import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any, Literal

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


class Node(BaseModel):
    """Represents a State or Event in the process"""
    id: str = Field(..., description="Unique identifier for the node (e.g., number, 'start', 'end').")
    type: Literal["state", "event"] = Field(..., description="Type of the node, either 'state' or 'event'.")
    description: str = Field(..., description="Brief explanation of the state or event.")

class Edge(BaseModel):
    """Represents a Trigger or Condition connecting Nodes"""
    from_node: str = Field(..., alias="from", description="ID of the starting node.")
    to: str = Field(..., description="ID of the target node.")
    type: str = Field(..., description="Type of the edge, either 'trigger' or 'condition'.")
    description: str = Field(..., description="Explanation of the trigger or condition.")

class Graph(BaseModel):
    """Graph structure containing all States, Events, Triggers, and Conditions"""
    nodes: List[Node] = Field(..., description="List of all states and events.")
    edges: List[Edge] = Field(..., description="List of all triggers and conditions.")





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
    you are 3gpp NAS procedure expert, help me with below task ,use knowledge of 3gpp procedure but strictly based on my instruction and provided text.
 I will provide you with two parts:  

1. **First part**: My extracted procedure flow property graph information about the 3GPP procedure "Registration procedure for initial registration."  
2. **Second part**: The original content of "Registration procedure for initial registration" from the 3GPP NAS specification.  

Please evaluate the accuracy and completeness of the extracted graph.

Your task:
Compare each node and edge in the JSON against the original document.
Identify any incorrect, missing, or misleading nodes or edges.
For each issue, give:
What’s wrong 
What it should be 
Why (with reference to the original sentence or paragraph)
You can also point out extra or irrelevant entries in the JSON.

**Strict Rule**: Use **only** the provided text. Do **not** infer or add missing details.  

Please return your evaluation as a JSON object.
For each identified issue, include:
"type": "node" or "edge"
"id" (or "from"/"to" for edges)
"what_is_wrong"
"suggested_fix"
"reason"
"reference_text": the sentence or paragraph from the original document that supports your reasoning
 "section_of_reference_text":the section where the reference text is located
Optionally include an "extras_or_irrelevant" section.

example json output format:
{{
  "issues": [
    {{
      "type": "node",  // or "edge"
      "id": "3",
      "what_is_wrong": "The decision node incorrectly links to node 4 on 'Success'.",
      "suggested_fix": "Should link to node 5 instead.",
      "reason": "Paragraph 5 states that after success, the process moves to step 5, not 4.",
      "reference_text": "After a successful registration, the UE initiates session setup..."
       "section_of_reference_text": "5.5.1.2.5"
    }},
    {{
      "type": "edge",
      "from": "2",
      "to": "3",
      "what_is_wrong": "Missing retry condition in case of timeout.",
      "suggested_fix": "Add an edge back to node 2 with reason 'Timeout, retry up to 3 times'.",
      "reason": "Section 2.1.4 mentions that on T3510 expiry, the UE retries registration up to 3 times.",
      "reference_text": "If the T3510 timer expires, the UE shall retransmit the request up to 3 times."
       "section_of_reference_text": "5.5.1.2.5"
    }}
  ],
  "extras_or_irrelevant": [
    {{
      "id": "6",
      "type": "node",
      "reason": "This node is not mentioned in the original document."
    }}
  ]
}}


Let’s begin.  

#### **Extracted procedure flow property graph info:**  

{json.dumps(extracted_data, indent=2)}

------------------
This is second part:
#### **orginal content from 3gpp specification:**  
{original_content}

remember Your task:
Compare each node and edge in the JSON against the original document.
Identify any incorrect, missing, or misleading nodes or edges.
For each issue, give:
What’s wrong
What it should be
Why (with reference to the original sentence or paragraph)
You can also point out extra or irrelevant entries in the JSON.

**Strict Rule**: Use **only** the provided text. Do **not** infer or add missing details.  

Please return your evaluation as a JSON object.
For each identified issue, include:
"type": "node" or "edge"
"id" (or "from"/"to" for edges)
"what_is_wrong"
"suggested_fix"
"reason"
"reference_text": the sentence or paragraph from the original document that supports your reasoning
Optionally include an "extras_or_irrelevant" section.

example json output format:
{{
  "issues": [
    {{
      "type": "node",  // or "edge"
      "id": "3",
      "what_is_wrong": "The decision node incorrectly links to node 4 on 'Success'.",
      "suggested_fix": "Should link to node 5 instead.",
      "reason": "Paragraph 5 states that after success, the process moves to step 5, not 4.",
      "reference_text": "After a successful registration, the UE initiates session setup..."
    }},
    {{
      "type": "edge",
      "from": "2",
      "to": "3",
      "what_is_wrong": "Missing retry condition in case of timeout.",
      "suggested_fix": "Add an edge back to node 2 with reason 'Timeout, retry up to 3 times'.",
      "reason": "Section 2.1.4 mentions that on T3510 expiry, the UE retries registration up to 3 times.",
      "reference_text": "If the T3510 timer expires, the UE shall retransmit the request up to 3 times."
       "section_of_reference_text": "5.5.1.2.5"
    }}
  ],
  "extras_or_irrelevant": [
    {{
      "id": "6",
      "type": "node",
      "reason": "This node is not mentioned in the original document."
    }}
  ]
}}
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
    
    extracted_data = read_json_file("v03-step3-complex-newmodel.json")
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
    save_to_txt(procedural_info, "v03-step4-evaluation.txt")
else:
    print("Failed to extract procedural information")
