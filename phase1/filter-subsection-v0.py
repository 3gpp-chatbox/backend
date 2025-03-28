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
You are a 3GPP specification procedure expert, well-versed in hierarchical structures and procedural extraction. Below is a list of sections from the NAS specification. Your task is to identify and list all sections that describe **sub-procedures**.

### **Definition of a Sub-Procedure**
A **sub-procedure** in 3GPP specifications is:  
1. A **logically self-contained but context-dependent** step within a larger procedure.  
2. It contributes **specific procedural functionality** that supports the execution of the main procedure.  
3. It **does not function independently** as a full procedure but plays a critical role in completing the parent procedure.  
4. **If a section has further sub-procedures, only extract its lowest valid sub-procedures** to avoid redundant selection.

### **Task Instructions**
- **Identify all sections that meet this definition.**
- **Only select the lowest-level valid sub-procedures**, meaning:
  - If a section has child sections that also qualify as sub-procedures, **do not select the parent**.  
  - The selected sections may have child sections, but these child sections **should not themselves describe sub-procedures.**

### **Sections to Analyze:**
{sections_str}

Please return **only** the section numbers that meet the criteria, with no additional text.
"""
    response = model.generate_content(prompt).text.strip()
    return response

# Main function to process files in a directory
def process_all_section_files(input_dir="initial_extracted_subsection", output_dir="filtered_subsections_v0"):
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