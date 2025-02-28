import sqlite3

# Step 1: Filter Procedure Sections from DB
def filter_procedure_sections(cursor):
    # Query the DB for all sections that contain the word 'Procedure'
    cursor.execute("""
        SELECT section_id, section_name, parent_section_id, section_level
        FROM section
        WHERE section_name LIKE '%Procedure%'
        ORDER BY section_id;
    """)
    
    # Fetch the filtered rows
    return cursor.fetchall()

# Step 2: Build procedure tree
def build_procedure_tree(procedure_sections):
    # Initialize procedure tree dictionary
    procedure_tree = {}

    # Construct the nodes for each section
    for row in procedure_sections:
        section_id, section_name, parent_section_id, section_level = row
        
        # Add the section as a node in the tree
        procedure_tree[section_id] = {
            "section_name": section_name,
            "parent_section_id": parent_section_id,
            "section_level": section_level,
            "children": []  # Placeholder for child sections
        }

    # Assign children to parent sections based on parent_section_id
    for section_id, section_data in procedure_tree.items():
        parent_id = section_data["parent_section_id"]
        if parent_id and parent_id in procedure_tree:
            procedure_tree[parent_id]["children"].append(section_id)
        else:
            print(f"Warning: Parent section {parent_id} not found for section {section_id}")

def merge_section_content(cursor, procedure_tree):
    # Step 1: Gather all section IDs to query content at once
    all_section_ids = list(procedure_tree.keys())

    # Step 2: Fetch all content chunks for these sections
    all_content = fetch_all_content(cursor, all_section_ids)

    section_content = {}

    for section_id, section_data in procedure_tree.items():
        print(f"Processing section {section_id}...")  # Debugging output

        # Fetch content for the current section from the pre-fetched content
        chunks = all_content.get(section_id, [])

        # If there is content for this section, merge it
        if chunks:
            full_content = "\n".join(chunks)
            section_content[section_id] = full_content
        else:
            # If no content found, set it to empty string or placeholder
            section_content[section_id] = ""  # or use: "No content available"

        # Process children even if the parent has no content
        if section_data["children"]:
            missing_children = [child_id for child_id in section_data["children"] if child_id not in procedure_tree]
            if missing_children:
                print(f"Warning: Missing children sections for {section_id}: {missing_children}")

            # Ensure children exist before recursion
            child_content = merge_section_content(cursor, {child_id: procedure_tree[child_id] for child_id in section_data["children"] if child_id in procedure_tree})
            
            # Merge content of children under the current section, if the section itself had no content
            if not section_content.get(section_id):  # If no content for the parent
                section_content[section_id] = ""  # Initialize it as an empty string

            section_content[section_id] += "\n\n" + "\n\n".join(child_content.values())

        # If no content was found for this section and no children, log a warning
        if not section_content.get(section_id):
            print(f"Warning: No content found for section {section_id}, but it may have children.")

    return section_content


# Main execution
conn = sqlite3.connect('section_content_0228.db')
cursor = conn.cursor()

# Step 1: Filter procedure sections
procedure_sections = filter_procedure_sections(cursor)

# Step 2: Build procedure tree
procedure_tree = build_procedure_tree(procedure_sections)

# Step 3: Merge parent and children content
section_content = merge_section_content(cursor, procedure_tree)

# Check merged content
for section_id, content in section_content.items():
    print(f"Section ID: {section_id}")
    print(f"Content: {content[:200]}...")  # Print a snippet for verification

# Close the database connection after operations are done
conn.close()

