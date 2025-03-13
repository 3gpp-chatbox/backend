import sqlite3

# Function to query the database and retrieve the full hierarchy for a section (parent, grandparent, etc.)
def query_section_hierarchy(section_id):
    hierarchy = []

    # Loop to retrieve parent sections up to level 1
    current_section = section_id
    while current_section:
        conn = sqlite3.connect('section_content_0310.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT section_id, section_name
            FROM sections
            WHERE section_id = ?
        ''', (current_section,))
        
        result = cursor.fetchone()
        if result:
            hierarchy.insert(0, result)  # Insert at the beginning to maintain order
            # Move up to the parent section by removing the last segment
            current_section = '.'.join(current_section.split('.')[:-1]) if '.' in current_section else None
        else:
            break
        conn.close()
    
    return hierarchy

# Function to query the database and get all subsections for a given section (Level 7)
def query_subsections(section_id_prefix):
    conn = sqlite3.connect('section_content_0310.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT section_id, section_name
        FROM sections
        WHERE section_id LIKE ?
    ''', (f'{section_id_prefix}%',))  # Wildcard search for subsections
    
    subsections = cursor.fetchall()
    conn.close()
    
    return subsections

# Function to send the data to LLM and retrieve extracted info
def send_to_llm(hierarchy, subsections):
    # For simplicity, simulate sending to LLM and returning extracted info
    # In real implementation, you will send hierarchy and subsections to the LLM via API
    print("Sending to LLM with hierarchy:")
    for section_id, section_name in hierarchy:
        print(f"Section ID: {section_id}, Section Name: {section_name}")
    
    print("Subsections:")
    for section_id, section_name in subsections:
        print(f"Section ID: {section_id}, Section Name: {section_name}")
    
    # Return simulated extracted info (in real implementation, this would be the LLM response)
    return f"Extracted info for subsections of {hierarchy[-1][0]}"

# Function to loop through the Level 7 sections and process them with full context
def process_procedures_with_context(level7_sections):
    for section_id, section_name in level7_sections:
        # 1. Query the hierarchy (parent, grandparent, etc.)
        hierarchy = query_section_hierarchy(section_id)
        
        # 2. Query the Level 7 subsections (this is the detailed section)
        subsections = query_subsections(section_id)
        
        # 3. Send the data (hierarchy + subsections) to the LLM for processing
        llm_output = send_to_llm(hierarchy, subsections)
        
        # Optionally, save the LLM output to a file
        with open(f"{section_id}_llm_output.txt", "w", encoding="utf-8") as file:
            file.write(llm_output)
        print(f"✅ Saved output for {section_id}.")

# Example Level 7 sections to process
level7_sections = [
    ("5.5.1.2.2", "Initial registration initiation"),
    ("5.5.1.3.3", "5GMM common procedure initiation"),
    ("5.5.2.2.6", "Abnormal cases in the UE"),
    # Add more Level 7 sections here...
]

# Process the procedures with context
process_procedures_with_context(level7_sections)
