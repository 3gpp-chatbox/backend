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


import re

# Function to read the sections from the file
def read_sections_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        sections = file.readlines()
    return sections

# Function to send sections to LLM with a classification prompt
def classify_sections_with_llm(sections):

      # Convert sections list to a single string that the model can process
    sections_str = "\n".join(sections)  # Join sections with newline


    prompt = f"""
You are a 3GPP specification procedure expert, and you understand procedures and specification structure very well. Below is a list of sections from the NAS specification. Your task is to identify and list all sections that describe **sub-procedures**.

A sub-procedure is defined as:
1. An independent step or phase within a larger procedure.
2. It can be logically separated and described on its own.
3. It is not a standalone procedure but is a significant component of a larger process.

Please list **all sections** that meet this definition, including those at deeper hierarchical levels 

Here is the list of sections:
{sections_str}

Please return only the sections that meet the criteria for sub-procedures.
"""

  
  

    response = model.generate_content(prompt).text.strip()
    with open('filtered_5.5_sections.txt', 'w', encoding='utf-8') as file:
        file.write(response)


    return response


# Main function to process
def process_sections():
    sections = read_sections_from_file('5.5_sections.txt')  # Read sections from the file
    
    classified_sections = classify_sections_with_llm(sections)  # Classify sections using LLM
    print(classified_sections) 
  

# Run the process
process_sections()