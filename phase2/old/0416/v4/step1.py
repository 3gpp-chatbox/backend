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
    
  I will provided your the original content of sections of 3gpp specification related to procedure"{section_name}"

    i want you to extract the flow property graph for this procedure"{section_name}" only on UE side. and return it in a structured format.

Core Components to Identify(remember only extract on UE side)

□ States: Different conditions or statuses of the UE, only extract explicitly state like 5GMM-DEREGISTERED,5GMM-REGISTERED.

elements.

Actions: Operations performed by the UE 

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or IDs.

Step1: identify and extract Key Steps in the procedure of UE side.
Step 2: Representing the Model as a Flow Property Graph 
A property graph consists of nodes (vertices) and edges, where both can have properties. This structure is suitable for representing complex relationships and flows.
Creating Nodes and Edges:
Nodes represent States and Events.
Edges represent Actions and Transitions, capturing the Flow of Execution.
□ Properties include Parameters, Conditionals, and Metadata.

Step 2: Attach procedure Nodes and Edges
(Example):
State Nodes:(Example data):UE_Powered_On UE_Attaching UE_Authenticating UE_Securing UE_Attached
Event Nodes:(Example data):Attach_Request_Received Authentication_Challenge Security_Mode_Command Attach_Accept_Received Attach_Complete_Sent Graph 
Edges:
Edges connect nodes to represent transitions triggered by actions or events.
Edge properties capture parameters, conditionals, and metadatá.


Step 3: Incorporating Conditionals and Parameters
Conditionals Decisions based on IMSI validation, security capabilities, etc.
Represented as properties or separate nodes in the graph.
Example Conditional:
If the authentication succeeds, proceed to security mode setup.
If it fails, reject the attach request.
Parameters and Metadata:
Parameters like !MSL Temporary.Mobile Subscriber Identity (fMSI), Tracking Area Identity (TAI).
Metadata such as timestamps, message identifiers.
Example:[UE_Authenticating] --(Condition: Auth_Success)--> [UE_Securing]
[UE_Authenticating] --(Condition: Auth_Failure)-->[Attach_Rejected]


only return json object in below format:
(EXAMPLE) 
   {{
  "nodes": [
    {{
      "id": "node1",
      "name": "UE_Powered_On",
      "type": "state",
      "properties": {{}}
    }},
    {{
      "id": "node2",
      "name": "UE_Attaching",
      "type": "state",
      "properties": {{}}
    }},
    {{
      "id": "node3",
      "name": "Attach_Request_Received",
      "type": "event",
      "properties": {{
        "message_type": "Attach Request"
      }},
      "parameters": ["IMSI", "TAI"]
    }}
  ],
  "edges": [
    {{
      "from": "UE_Powered_On",
      "to": "UE_Attaching",
      "action": "Send_Attach_Request",
      "properties": {{
        "parameters": ["IMSI", "TAI"],
        "metadata": {{
          "timestamp": "T0"
        
        }}
      }},
      "condition": "None"
      "section_reference":"5.2.4.2.1"
    
    }},
    {{
      "from": "UE_Attaching",
      "to": "Attach_Request_Received",
     
      "action": "Send_Attach_Request",
      "properties": {{}},
      "condition": "condition"
        "section_reference":"5.2.4.2.1"
        
    }},
    {{
      "from": "UE_Authenticating",
      "to": "UE_Securing",
      "action": "Initiate_Authentication",
      "properties": {{
        "parameters": ["IMSI", "TAI"],
        "metadata": {{
          "timestamp": "T1"
        }}
      }},
      "condition": "Auth_Success"
      "section_reference":"5.2.1.2.1"
   
    }},
    {{
      "from": "UE_Authenticating",
      "to": "Attach_Rejected",
      "action": "Send_Authentication_Failure",
      "properties": {{
        "parameters": ["IMSI", "TAI"],
        "metadata": {{
          "timestamp": "T2"
        }}
      }},
      "condition": "Auth_Failure"
       "section_reference":"3.2.1.3"
    
    }}
  ]
}}
only return json code.
----
This is original content , only analyze based on my provided text, do not make assumption.
:

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
    save_procedural_info_to_json(procedural_info, "step1.json")
else:
    print("Failed to extract procedural information")

if save_procedural_info_to_json:
   clean_json("step1.json")
else:
    print("Failed to clean json file")