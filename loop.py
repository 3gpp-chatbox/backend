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

import sqlite3

def get_hierarchical_content(section_id):
    conn = sqlite3.connect('section_content_0310.db')
    cursor = conn.cursor()

    levels = section_id.split('.')
    related_sections = []

    # Find sibling "General" sections
    if len(levels) > 1:
        parent_level = '.'.join(levels[:-1]) + '.%' # create parent level wildcard
        cursor.execute('''
            SELECT section_id, section_name, content_chunk
            FROM content
            WHERE section_id LIKE ? AND section_name = 'General'
        ''', (parent_level,))
        sibling_general_results = cursor.fetchall() #Fetch all results
        if sibling_general_results:
            related_sections.extend(sibling_general_results) # add all found general sections

    # Extract the regular hierarchy (parents, grandparents, etc.)
    for i in range(len(levels), 0, -1):
        section_prefix = '.'.join(levels[:i])
        cursor.execute('''
            SELECT section_id, section_name, content_chunk
            FROM content
            WHERE section_id = ?
        ''', (section_prefix,))
        result = cursor.fetchone()
        if result:
            related_sections.append(result)

    conn.close()
    return related_sections

# Function to send hierarchical content to LLM
def extract_procedure_from_llm(section_id, content_hierarchy):
    prompt = """
    You are a **3GPP NAS specification expert** analyzing procedural flows from technical documentation.  
    Below is a **hierarchical section structure**, including parent sections for context.  

    Your task: **Extract a structured procedure** by identifying:  
    - **Triggering Conditions:** When and why the procedure starts.  
    - **Signaling Steps:** Include specific **NAS messages** (e.g., REGISTRATION REQUEST, AUTHENTICATION RESPONSE).  
    - **Decision Points:** Clearly define logical branches (e.g., authentication required? → Yes/No).  
    - **Information Elements (IEs):** Extract key elements that impact the procedure.  
      
    **Hierarchical Section Context:**  
    """
    for sec_id, sec_name, content_chunk in content_hierarchy:
        prompt += f"Section {sec_id}: {sec_name}\n{content_chunk}\n\n"
    
    prompt += """
    **Expected Output Format:**
    - **Procedure Name:** <Name>
    - **Triggering Conditions:**
        - Condition 1
        - Condition 2
    - **Steps:**
        1. Step description
        2. Step description
    - **Decision Points:**
        - Decision 1 → Outcome A / Outcome B
    - **State Transitions:**
        - After step 1, the state is <STATE>
        - After step 3, the state is <STATE>
    - **Important Information Elements:**
        - IE 1: Description
        - IE 2: Description
    """

      # Save the whole prompt to a file
    prompt_file = f"prompts/{section_id}_prompt.txt"
    os.makedirs("prompts", exist_ok=True)
    with open(prompt_file, 'w', encoding='utf-8') as prompt_out_file:
        prompt_out_file.write(prompt)
    
    response = model.generate_content(prompt).text.strip()
    return response

# Function to process sections from file
def process_sections_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]  # Skip header
    
    for line in lines:
        section_id, section_name = line.strip().split(', ', 1)
        
        if section_name.lower() == "general":
            print(f"⏭️ Skipping {section_id} ({section_name})")
            continue  # Skip general sections
        
        print(f"🔍 Processing {section_id} ({section_name})")
        
        # Retrieve hierarchical context
        hierarchy = get_hierarchical_content(section_id)
        
        # Extract procedures using LLM
        procedure_info = extract_procedure_from_llm(section_id, hierarchy)
        
        # Save result
        output_file = f"procedures/{section_id}_procedure.txt"
        os.makedirs("procedures", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(procedure_info)
        
        print(f"✅ Saved procedure for {section_id} in {output_file}")

# Run the process
test_file = "5.5_sections.txt"
process_sections_from_file(test_file)
