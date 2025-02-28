import sqlite3

# Step 1: Filter Procedure Sections
def filter_procedure_sections():
    with sqlite3.connect('section_content_0228.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT section_id, section_name, parent_section_id, parent_section_name, section_level 
            FROM sections 
            WHERE section_name LIKE '%Procedure%'
            ORDER BY section_id;
        ''')
        return cursor.fetchall()


# Step 2: Build Recursive Tree
def build_recursive_tree(procedure_sections):
    section_dict = {}

    # Store all sections in dictionary
    for section in procedure_sections:
        section_id, section_name, parent_section_id, parent_section_name, section_level = section
        section_dict[section_id] = {
            "section_name": section_name,
            "parent_section_id": parent_section_id,
            "children": [],
            "section_level": section_level
        }

    # Assign children to parents
    for section_id, section_data in section_dict.items():
        parent_id = section_data["parent_section_id"]
        if parent_id in section_dict:
            section_dict[parent_id]["children"].append(section_id)

    return section_dict


# Step 3: Fetch Content
def fetch_content(section_id):
    with sqlite3.connect('section_content_0228.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT content_chunk FROM content WHERE section_id = ? ORDER BY content_id
        ''', (section_id,))
        chunks = cursor.fetchall()
        return "\n".join(chunk[0] for chunk in chunks if chunk[0])


# Step 4: Merge Parent + Children Content 🌶️
def merge_content(tree, section_id):
    content = fetch_content(section_id)

    # Merge Children Content 🔥 Recursively
    for child_id in tree[section_id]["children"]:
        content += "\n\n" + merge_content(tree, child_id)

    return content




# Main Execution Pipeline 🔥
if __name__ == '__main__':
    # Step 1: Filter Procedure Sections
    procedure_sections = filter_procedure_sections()
    print(f"Total Procedure Sections Found: {len(procedure_sections)}")

    # Step 2: Build Tree
    procedure_tree = build_recursive_tree(procedure_sections)
    print(f"Total Parent Sections: {len([k for k, v in procedure_tree.items() if v['children']])}")

    # Step 3: Merge Content for All Sections
    for section in procedure_sections:
        section_id = section[0]
        merged_content = merge_content(procedure_tree, section_id)
        print(f"✅ Merged Content Length for Section {section_id}: {len(merged_content)}")
