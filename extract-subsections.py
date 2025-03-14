import sqlite3
import re

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
    
    cursor.execute('''
        SELECT section_id, section_name
        FROM sections
        WHERE section_id LIKE ? and section_level IN (3, 4, 5)
    ''', (f'{section_id_prefix}%',))  
    
    sections = cursor.fetchall()
    conn.close()
    
    return sections

# Save query results to file
def save_to_file(section_id_prefix, sections):
    filename = f"{section_id_prefix}_sections.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("Section ID, Section Name\n")
        for section_id, section_name in sections:
            file.write(f"{section_id}, {section_name}\n")
    print(f"✅ Saved to {filename}")

# Main function to process
def process_sections_from_llm():
    # Step 1: Extract Level 2 sections from LLM output
    level2_sections = extract_level2_sections('llmoutput.txt')

    # Step 2: Query DB and save to file for each Level 2 section
    for section in level2_sections:
        subsections = query_sections(section)
        save_to_file(section, subsections)

# Run the process
process_sections_from_llm()
