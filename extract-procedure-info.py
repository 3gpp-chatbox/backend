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

import sqlite3
import sqlite3
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')

def get_hierarchical_content(section_id):
    conn = sqlite3.connect('section_content_0310.db')
    cursor = conn.cursor()

    levels = section_id.split('.')
    related_sections = []

    # Get the target section's content
    cursor.execute('''
        SELECT section_name, content_chunk
        FROM content
        WHERE section_id = ?
    ''', (section_id,))
    target_section = cursor.fetchone()

    if not target_section:
        conn.close()
        return None, []  # Return None and empty list if target section not found

    # Extract the regular hierarchy (parents, grandparents, etc.) in correct order
    for i in range(1, len(levels) + 1): #change the range to get the correct order.
        section_prefix = '.'.join(levels[:i])
        cursor.execute('''
            SELECT section_id, section_name, content_chunk
            FROM content
            WHERE section_id = ?
        ''', (section_prefix,))
        result = cursor.fetchone()
        if result:
            related_sections.append(result)

    # Find sibling "General" sections
    if len(levels) > 1:
        parent_level = '.'.join(levels[:-1]) + '.%'
        cursor.execute('''
            SELECT section_id, section_name, content_chunk
            FROM content
            WHERE section_id LIKE ? AND section_name = 'General'
        ''', (parent_level,))
        sibling_general_results = cursor.fetchall()
        if sibling_general_results:
            related_sections.extend(sibling_general_results)

    conn.close()
    return target_section, related_sections

def extract_procedure_from_llm(section_id, target_section, content_hierarchy):
    if not target_section:
        return "Target section not found."

    target_name, target_content = target_section
    prompt = f"""
    You are a **3GPP NAS specification expert** analyzing procedural flows from technical documentation.

    Below is a **hierarchical section structure**, including parent sections for context.

    our target section to extract procedure is: {section_id} {target_name},

    its content is:
    {target_content}

    above is our main target sections content to extract procedure, and then below is **Hierarchical Section Context surrounding it, i send them to you for you to understand the relationship and document strcuture and may contain some info you need for help you to extract procedure in the target section better:**
    """

    # Exclude the target section from the hierarchy
    for sec_id, sec_name, content_chunk in content_hierarchy:
        if sec_id != section_id: #add this line to exclude the target section.
            prompt += f"\nSection {sec_id}: {sec_name}\n{content_chunk}\n"

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

    prompt_file = f"prompts/{section_id}_prompt.txt"
    os.makedirs("prompts", exist_ok=True)
    with open(prompt_file, 'w', encoding='utf-8') as prompt_out_file:
        prompt_out_file.write(prompt)

    response = model.generate_content(prompt).text.strip()
    return response

def process_sections_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]

    for line in lines:
        section_id, section_name = line.strip().split(', ', 1)

        if section_name.lower() == "general":
            print(f"⏭️ Skipping {section_id} ({section_name})")
            continue

        print(f"🔍 Processing {section_id} ({section_name})")

        target_section, hierarchy = get_hierarchical_content(section_id)

        procedure_info = extract_procedure_from_llm(section_id, target_section, hierarchy)

        output_file = f"procedures/{section_id}_procedure.txt"
        os.makedirs("procedures", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write(procedure_info)

        print(f"✅ Saved procedure for {section_id} in {output_file}")

test_file = "5.5_sections.txt"
process_sections_from_file(test_file)