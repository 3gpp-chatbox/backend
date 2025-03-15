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
You are a 3GPP specification procedure expert. Your task is to identify and list all leaf-level sub-procedures from the following sections of the NAS specification.

Definition of a Leaf-Level Sub-Procedure
A leaf-level sub-procedure in 3GPP specifications is:
1. A logically self-contained, context-dependent step within a larger procedure.
2. It contributes specific procedural functionality to the parent procedure but does not function independently as a complete procedure.
3. It is at the **end of the hierarchical chain** or as close as possible to the end, meaning it has no further divisions that describe additional independent sub-procedures within it.
4. If a section has child sections that describe specific steps or edge cases, these are still part of the leaf-level sub-procedure if they do not introduce new independent sub-procedures.

Task Instructions:
Identify and list only the leaf-level sub-procedures. These are the sections that do not have any further independent sub-procedures within them, even if they have child sections describing steps, edge cases, or abnormal situations.

Sections List to Analyze:
{sections_str}

Please return only the section ID and name of the leaf-level sub-procedures, without any additional explanation or text.



"""
    response = model.generate_content(prompt).text.strip()
    return response

# Main function to process files in a directory
def process_all_section_files(input_dir="initial_extracted_subsection", output_dir="filtered_subsections-v2"):
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