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

# Function to retrieve hierarchical content from the database
def get_hierarchical_content(section_id):
    conn = sqlite3.connect('section_content_0310.db')
    cursor = conn.cursor()
    
    # Extract hierarchy (parents, grandparents, etc.)
    levels = section_id.split('.')
    related_sections = []
    
    for i in range(len(levels), 0, -1):
        section_prefix = '.'.join(levels[:i])
        cursor.execute('''
            SELECT section_id, section_name, content_chunk FROM content WHERE section_id = ?
        ''', (section_prefix,))
        result = cursor.fetchone()
        if result:
            related_sections.append(result)
    
    conn.close()
    return related_sections

# Function to send hierarchical content to LLM
def extract_procedure_from_llm(section_id, content_hierarchy):
    prompt = """
    You are a 3GPP expert analyzing NAS specification procedures.
    Below is the hierarchical structure of a section, including its parents and context:
    
    """
    for sec_id, sec_name, sec_content in content_hierarchy:
        prompt += f"Section {sec_id}: {sec_name}\n{sec_content}\n\n"
    
    prompt += "Extract the key procedural steps from this context."


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
