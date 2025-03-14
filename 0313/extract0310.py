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

# Function to query the sections table and generate the ToC file
def extract_sections():
    # Connect to SQLite database
    conn = sqlite3.connect('section_content_0310.db')
    cursor = conn.cursor()

    # Query to retrieve level 1, 2, and 3 sections
    cursor.execute('''
    SELECT section_id, section_name
    FROM sections
    WHERE section_level IN (1, 2, 3,4)
    ''')

    # Fetch all results
    sections = cursor.fetchall()

    # Prepare content to write to a new file
    output_content = "Section ID, Section Name\n"  # Adding header to the output file
    for section in sections:
        section_id, section_name = section
        output_content += f"{section_id}, {section_name}\n"

    # Write the results to a new file
    with open('sections_level_1_2_3.txt', 'w', encoding='utf-8') as file:
        file.write(output_content)

    # Close the database connection
    conn.close()

    print("✅ Level 1, 2, and 3 sections saved to 'sections_level_1_2_3.txt'.")

    return output_content  # Return the content for further use


# Function to query sections and ask LLM to list sections with procedures
def find_section_with_procedure_info():
    # First, extract the sections
    output_content = extract_sections()  # Get the extracted sections from the previous function

    # Create the prompt for LLM
    prompt = f"""
    You are a 3GPP expert and an expert in NAS specification procedures.you know very well about the structure of the document.
    Here are the NAS specification document sections:

    {output_content}

    as you can see section heading has different levels, and section is nested structure.based on your knowledge about 3GPP specification document structure,
    Please based on the text i provided above to list the sections  that contain procedures.only return section id and name .only return  section heading is level2(like 1.1, 2.2,x.x)
    """

    # Assuming you have an LLM client or API for interacting with Google AI Gemini
    # Example using fictional API call:
    # response = model.generate_content(prompt).text.strip()  # Adjust this based on your LLM service

    response = model.generate_content(prompt).text.strip()
    # Save LLM response to a file
    with open('llmoutput.txt', 'w', encoding='utf-8') as file:
        file.write(response)

    print("✅ LLM output saved to 'llmoutput.txt'.")
    
    return response  # Return the response from the LLM


# Call the function to extract sections and find those containing procedures
find_section_with_procedure_info()


