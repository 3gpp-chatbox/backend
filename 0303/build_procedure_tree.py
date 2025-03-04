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

    return procedure_tree

# Build the tree from the filtered sections
procedure_tree = build_procedure_tree(procedure_sections)
print(procedure_tree)
