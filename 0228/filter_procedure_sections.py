import sqlite3

import sqlite3

def filter_procedure_sections():
    conn = sqlite3.connect('section_content_0228.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT section_id, section_name, parent_section_id, parent_section_name, section_level 
        FROM sections 
        WHERE section_name LIKE '%Procedure%'
        ORDER BY section_id;
    ''')

    sections = cursor.fetchall()
    conn.close()

    return sections

procedure_sections = filter_procedure_sections()
print(f"Total Procedure Sections Found: {len(procedure_sections)}")


# Step 2: Build procedure tree
def build_recursive_tree(procedure_sections):
    section_dict = {}

    # Step 1: Store all sections in dictionary
    for section in procedure_sections:
        section_id, section_name, parent_section_id, parent_section_name, section_level = section
        section_dict[section_id] = {
            "section_name": section_name,
            "parent_section_id": parent_section_id,
            "children": [],
            "section_level": section_level
        }

    # Step 2: Assign children to parents
    for section_id, section_data in section_dict.items():
        parent_id = section_data["parent_section_id"]
        if parent_id in section_dict:
            section_dict[parent_id]["children"].append(section_id)

    return section_dict

procedure_tree = build_recursive_tree(procedure_sections)
print(f"Total Parent Sections: {len([k for k, v in procedure_tree.items() if v['children']])}")

def fetch_content(section_id):
    conn = sqlite3.connect('section_content_0228.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT content_chunk FROM content WHERE section_id = ? ORDER BY content_id
    ''', (section_id,))
    chunks = cursor.fetchall()
    conn.close()

    content = "\n".join(chunk[0] for chunk in chunks if chunk[0])
    return content

def merge_content(tree, section_id):
    content = fetch_content(section_id)

    # Merge children recursively
    for child_id in tree[section_id]["children"]:
        content += "\n\n" + merge_content(tree, child_id)

    return content

# Example: Merge Content for One Procedure Section
section_id = procedure_sections[0][0]
merged_content = merge_content(procedure_tree, section_id)
print(f"Content Length for Section {section_id}: {len(merged_content)}")



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

