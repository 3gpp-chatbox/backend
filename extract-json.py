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
    You are a **3GPP NAS expert** converting structured procedural steps into a JSON-based **Flow Property Graph (FPG)**.
    
    **Instructions:**  
    1. **Identify Key Nodes:** Extract distinct procedural steps as **Nodes**, classified as:  
       - **Event:** When something occurs (e.g., "UE sends REGISTRATION REQUEST").  
       - **Decision:** When a condition determines different paths (e.g., "Is authentication required?").  
       - **Action:** A specific operation performed by an entity (e.g., "AMF starts authentication"). 
       - **State:** A defined state of an entity (e.g., "UE in DEREGISTERED state").   
      
    2. **Define Transitions (Edges):** Ensure logical links between nodes with **clear conditions**.  

    **Procedure Steps:**
    {procedure_content}

    **Expected JSON Output Format:**  
    {{
      "procedure_name": "<Procedure Name>",
      "nodes": [
        {{
          "id": "<Node_ID>",
          "type": "<Event/Decision/Action>",
          "entity": "<UE/AMF/etc.>",
          "description": "<Step description>"
        }}
      ],
      "edges": [
        {{
          "source": "<Node_ID>",
          "target": "<Node_ID>",
          "condition": "<Condition for transition>"
        }}
      ]
    }}
    
    **Key Considerations:**
    - **Use correct NAS messages** (e.g., AUTHENTICATION REQUEST, SECURITY MODE COMMAND).  
    - **Ensure all decision nodes have at least two outcomes** (e.g., "Yes → Node A, No → Node B").  
    - **Maintain logical flow** so that procedures do not break.  

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
