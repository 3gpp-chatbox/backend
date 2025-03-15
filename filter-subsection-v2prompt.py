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

A logically self-contained, context-dependent step within a larger procedure.
It contributes specific procedural functionality to the parent procedure but does not function independently as a complete procedure.
It is at the end of the hierarchical chain, meaning there are no further subdivisions that describe additional sub-procedures within it.
If a section has child sections, they may describe steps or exception cases but do not constitute new sub-procedures.
Task Instructions
Identify and list only the leaf-level sub-procedures.
These are the sub-procedures that are not subdivided further into independent sub-procedures.
If a section has children that provide more details or edge cases, it still counts as a leaf-level sub-procedure.
Sections List to Analyze:
{sections_str}

Please return only the section ID and name of the leaf-level subprocedures, without any additional explanation or text.


"""
    response = model.generate_content(prompt).text.strip()
    return response

# Main function to process files in a directory
def process_all_section_files(input_dir="initial_extracted_subsection", output_dir="filtered_subsections_promptv2"):
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