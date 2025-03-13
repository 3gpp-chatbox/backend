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
def generate_flow_property_graph(procedure_content):
    prompt = f"""
    Based on the following procedure information, generate a Flow Property Graph (FPG) in JSON format:

    {procedure_content}
    
    The flow property graph should include nodes and edges representing the procedure steps, conditions, and relations.
    Return the result as a valid JSON object.
    Core Components to Identify

□ States: Different conditions or statuses of the UE and network

elements.

Actions: Operations performed by the UE or network.

Events: Triggers causing transitions between states.

Parameters: Data exchanged or required during the procedure.

Flow of Execution: Sequence of steps in the procedure.

Conditionals: Decisions based on certain criteria or parameters.

Metadata: Additional information like timestamps, message types, or

IDs.

(this is an json example of a procedure example):

     {{
      "procedure_name": "procedure name here ",
  "description": " description here  ",
 
      "nodes": [
        {{
          "id": "UE_Powered_On",
          "type": "state",
          "properties": {{}}
        }},
        {{
          "id": "UE_Attaching",
          "type": "state",
          "properties": {{}}
        }},
        {{
          "id": "Attach_Request_Received",
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
          }}
        }},
        {{
          "from": "UE_Attaching",
          "to": "MME_Processing",
          "event": "Attach_Request_Received",
          "properties": {{}}
        }}
      ]
    }}
    """

    # Send the prompt to LLM
      
    response = model.generate_content(prompt).text.strip()

    # Clean up the response by removing ```json and the closing ```
    response_cleaned = re.sub(r"^```json\s*", "", response)  # Remove leading ```json
    response_cleaned = re.sub(r"```$", "", response_cleaned)  # Remove trailing ```

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
