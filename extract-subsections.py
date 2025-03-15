import sqlite3
import re
import os
import sqlite3
import re
import os

# Function to read LLM output and extract only Level 2 sections (e.g., 5.4, 5.5, 6.4, 6.6)
def extract_level2_sections(llm_output_file):
    with open(llm_output_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex pattern to match only Level 2 headings like 5.4, 5.5, 6.3, 6.4, 6.5
    pattern = r'(\d+\.\d+),\s*(.*)'
    matches = re.findall(pattern, content)
    
    # Extract section IDs (e.g., 5.4, 5.5, 6.4)
    level2_sections = [match[0] for match in matches if len(match[0].split('.')) == 2]

    return level2_sections

# Query database to get all sections under a given section (e.g., 5.5.*)
def query_sections(section_id_prefix):
    conn = sqlite3.connect('section_content_0310.db')
    cursor = conn.cursor()
    
    # Query for subsections (e.g., 5.4, 5.4.1, 5.4.2, etc.)
    cursor.execute('''
        SELECT section_id, section_name
        FROM sections
        WHERE section_id LIKE ? AND section_level IN (2, 3, 4, 5, 6, 7)
    ''', (f'{section_id_prefix}%',))
    
    subsections = cursor.fetchall()
    
    # Query for the parent section (e.g., 5)
    parent_section_id = section_id_prefix.split('.')[0]  # Extract parent ID (e.g., 5 from 5.4)
    cursor.execute('''
        SELECT section_id, section_name
        FROM sections
        WHERE section_id = ? AND section_level = 1
    ''', (parent_section_id,))
    
    parent_section = cursor.fetchone()
    
    conn.close()
    
    # Combine parent section and subsections
    if parent_section:
        return [parent_section] + subsections
    else:
        return subsections

# Save query results to file
def save_to_file(section_id_prefix, sections, output_dir):
    filename = os.path.join(output_dir, f"{section_id_prefix}_sections.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Section ID, Section Name\n")
        for section_id, section_name in sections:
            file.write(f"{section_id}, {section_name}\n")
    print(f"✅ Saved to {filename}")

# Main function to process
def process_sections_from_llm(output_dir="initial_extracted_subsection"):
    os.makedirs(output_dir, exist_ok=True)  # Creates the folder if it does not exist.
    
    # Step 1: Extract Level 2 sections from LLM output
    level2_sections = extract_level2_sections('refined-llmoutput.txt')

    # Step 2: Query DB and save to file for each Level 2 section
    for section in level2_sections:
        sections = query_sections(section)
        save_to_file(section, sections, output_dir)

# Run the process
process_sections_from_llm()