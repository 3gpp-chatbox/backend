
#step3 Step 3: Merge Parent + All Children Content

def merge_section_content(cursor, procedure_tree):
    section_content = {}

    # Loop through each section in the procedure tree
    for section_id, section_data in procedure_tree.items():
        # Fetch content for the current section
        cursor.execute("""
            SELECT content_chunk
            FROM content
            WHERE section_id = ? 
            ORDER BY chunk_id
        """, (section_id,))
        chunks = cursor.fetchall()

        # Merge all content chunks
        full_content = "\n".join(chunk[0] for chunk in chunks)
        section_content[section_id] = full_content
        
        # Recursively merge content from child sections
        if section_data["children"]:
            child_content = merge_section_content(cursor, {child_id: procedure_tree[child_id] for child_id in section_data["children"]})
            section_content[section_id] += "\n\n" + "\n\n".join(child_content.values())

    return section_content

# Merge content for all procedure sections
conn = sqlite3.connect('section_content_0228.db')
cursor = conn.cursor()

section_content = merge_section_content(cursor, procedure_tree)
conn.close()

# Check the merged content
for section_id, content in section_content.items():
    print(f"Section ID: {section_id}")
    print(f"Content: {content[:200]}...")  # Print a snippet for verification

