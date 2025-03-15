import sqlite3
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to read the sections from the file
def read_sections_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        sections = file.readlines()
    return sections

# Function to send sections to LLM with a classification prompt
def classify_sections_with_llm(sections):
    sections_str = "\n".join(sections)
    prompt = f"""
You are a 3GPP specification procedure expert, and you understand procedures and specification structure very well. Below is a list of sections from the NAS specification. Your task is to identify and list all sections that describe **sub-procedures**.

A sub-procedure is defined as:
1. An independent step or phase within a larger procedure.
2. It can be logically separated and described on its own.
3. It is not a standalone procedure but is a significant component of a larger process.


Please list **all sections** that meet this definition, where the child sections do not describle subprocedure that we defined above, which means, the sections you are going to list contain the lowest level sub-procedure. the section you need extract and list, they might have child section (sub section),but their child sections cannot be the sections that describle sub-procedures we defined above.

Here is the list of sections:
{sections_str}

Please return only the sections that meet the criteria .
"""
    response = model.generate_content(prompt).text.strip()
    return response

# Main function to process files in a directory
def process_all_section_files(input_dir="initial_extracted_subsection", output_dir="filtered_subsections"):
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return

    for filename in os.listdir(input_dir):
        if filename.endswith('_sections.txt'):
            file_path = os.path.join(input_dir, filename) #Input file path is now in the input dir.
            sections = read_sections_from_file(file_path)
            classified_sections = classify_sections_with_llm(sections)

            output_filename = filename.replace('.txt', '_filtered.txt')
            output_filepath = os.path.join(output_dir, output_filename)

            with open(output_filepath, 'w', encoding='utf-8') as output_file:
                output_file.write(classified_sections)

            print(f"✅ Filtered sections saved to {output_filename}")

# Run the process
process_all_section_files()