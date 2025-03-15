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

with open("llmoutput.txt", 'r', encoding='utf-8') as file:
        content = file.read()

with open("sections_level_1_2_3.txt", 'r', encoding='utf-8') as file:
    original_sections = file.read()

def find_section_with_procedure_info():

    # Create the prompt for LLM
    prompt = f"""
    You are a 3GPP expert and an expert in NAS specification procedures.you know very well about the structure of the document.
    I asked llm to extract sections containing procedures information from all sections name of document.

    this is what i provided to it:
    {original_sections}
    
    and this is the result it gave:
    {content}

    you are 3gpp specification expert, please analyze based on the original section list and the extracted result list,then return your refined list of sections if the result is not correct ,only return sections that contain procedures,only return correct section id and section name in your response(use , to split id and name),do not include any other words in your response.
    """

    # Assuming you have an LLM client or API for interacting with Google AI Gemini
    # Example using fictional API call:
    # response = model.generate_content(prompt).text.strip()  # Adjust this based on your LLM service

    response = model.generate_content(prompt).text.strip()
    # Save LLM response to a file
    with open('refined-llmoutput.txt', 'w', encoding='utf-8') as file:
        file.write(response)

    print("✅ LLM output saved to 'refined-llmoutput.txt'.")
    
    return response  # Return the response from the LLM


# Call the function to extract sections and find those containing procedures
find_section_with_procedure_info()