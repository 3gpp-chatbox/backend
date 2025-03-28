import json
import sqlite3

import sqlite3
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import json
import os
from pydantic import BaseModel, ValidationError, Field,model_validator
from typing import List, Dict, Optional, Any 
import sys
import time
from enum import Enum

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to generate Flow Property Graph (FPG) using LLM based on procedure content
import re

def generate_flow_property_graph(procedure_content):
    prompt = f"""
    "Analyze the 3GPP NAS procedure text I provided first:

    {procedure_content}

    Remember, all your analysis should be based on the chunk text i provided, and you should not make any assumptions.
    and then extract a Flow Property Graph (FPG) in JSON format. The FPG should represent the following core components:

    States: UE and Network states during the procedure (e.g., EMM-Registered, EMM-Deregistered).
    Events: NAS message exchanges or internal events that cause transitions.
    Actions: Operations triggered by events (e.g., sending Attach Request).
    Parameters: NAS message fields (e.g., IMSI, TAI, GUTI).
    Conditionals: Branching logic or decision points based on NAS information.
    Flow of Execution: Sequence of state transitions.
    Metadata: Message types, timestamps, or UE IDs.
    The JSON format should follow this exact structure:


    {{
    "procedure_name": "Attach Procedure",
    "description": "The initial attach procedure in 5G NAS.",
    "nodes": [
        {{
        "id": "UE_Powered_On",
        "type": "state",
        "properties": {{}}
        }},
        {{
        "id": "Attach_Request_Sent",
        "type": "event",
        "properties": {{
            "message_type": "NAS Attach Request"
        }},
        "parameters": ["IMSI", "GUTI"]
        }},
        {{
        "id": "MME_Processing",
        "type": "state",
        "properties": {{}}
        }}
    ],
    "edges": [
        {{
        "from": "UE_Powered_On",
        "to": "Attach_Request_Sent",
        "action": "Send_Attach_Request",
        "properties": {{
            "metadata": {{
            "timestamp": "T0"
            }},
            "parameters": ["IMSI", "GUTI"]
        }}
        }},
        {{
        "from": "Attach_Request_Sent",
        "to": "MME_Processing",
        "event": "Attach_Request_Received",
        "properties": {{}}
        }}
    ],
    "conditionals": [
        {{
        "condition": "If IMSI is valid",
        "next_state": "Authentication Procedure"
        }}
        ]
    }}

    only return json in your response.
    """
    # Assuming 'model' is defined somewhere (like an LLM API client)
    response = model.generate_content(prompt).text.strip() # Example, replace with your actual LLM call.
   
    response_cleaned = re.sub(r"^```json\s*", "", response)
    response_cleaned = re.sub(r"```$", "", response_cleaned)

    response_cleaned = response_cleaned.strip()

    return response_cleaned


# Function to process each procedure file and generate corresponding FPG in JSON format
def generate_fpg_from_procedures(procedures_folder="procedures"):
    # Loop through all the procedure files in the procedures folder
    for file_name in os.listdir(procedures_folder):
        if file_name.endswith(".txt"):
            section_id = file_name.split('_')[0]  # Extract section_id from the file name (e.g., "5.5.1")
            
            # Read the procedure content from the file
            procedure_file_path = os.path.join(procedures_folder, file_name)
            with open(procedure_file_path, 'r', encoding='utf-8') as file:
                procedure_content = file.read()
            
            # Generate the Flow Property Graph based on the procedure content
            fpg = generate_flow_property_graph(procedure_content)
            
            # Save the generated FPG as a new JSON file
            output_fpg_file = f"fpgs/{section_id}_fpg.json"
            os.makedirs("fpgs", exist_ok=True)
            with open(output_fpg_file, 'w', encoding='utf-8') as file:
                file.write(fpg)
            
            print(f"✅ Saved FPG for {section_id} in {output_fpg_file}")

# Run the process for generating FPGs
generate_fpg_from_procedures()
