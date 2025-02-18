import sys
from main_processor import (
    extract_section_tree, 
    load_document, 
    extract_paragraphs,
    create_chunks_with_context,
    process_chunks_and_extract_graph
)
import os
from textChunker import TextChunker
import json

def main():    
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_folder, "config.py")   
    docx_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.docx")

    #  load the document
    doc = load_document(docx_path)
    # extract sections
    sections = extract_section_tree(doc)

    if doc:
        sections = extract_section_tree(doc)
        chunks = create_chunks_with_context(sections)
        target_procedure = "Attach Procedure"
        # Save the chunks to a JSON file
    #     with open("document_chunks_langchain.json", "w", encoding="utf-8") as f:
    #         json.dump(chunks, f, indent=4)

    # print("Document chunks (LangChain) saved to document_chunks_langchain.json")
        graph_data = process_chunks_and_extract_graph(chunks, target_procedure)

    with open("nas_nr_graph.json", "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=4)

    print("NAS NR graph data saved to nas_nr_graph.json")


    # save the structured data to a json file
    # with open("document_sections.json", "w", encoding="utf-8") as f:
    #     json.dump([section.__dict__ for section in sections], f, default=str) 

    # print("Document sections saved to document_sections.json")



    #------------ print the structure of section tree----------------------
    # print(f"\nFound {len(sections)} top-level sections:")

    # for para in paragraphs:
    #     if "annex b" in para['text'].lower():
    #         print(para['style'])
    #         print(para['text'])
    #         print("*" * 80)


    # def get_section_content_length(section):
    #     # Get max content length from individual chunks in current section
    #     current_length = max((len(chunk) for chunk in section.content), default=0) if hasattr(section, 'content') else 0
        
    #     # Recursively get content length of subsections
    #     subsection_lengths = [get_section_content_length(subsec) for subsec in section.subsections]
        
    #     # Return the maximum length found
    #     return max([current_length] + subsection_lengths)

    # def print_section_tree(section, file, indent_level=0, parent_heading=None):
    #     indent = "  " * indent_level
    #     connector = "└─ " if indent_level > 0 else ""
        
    #     # Write current section info to file
    #     section_type = "Top Level Section" if indent_level == 0 else "Section"
    #     file.write(f"\n{indent}{connector}{section_type}: {section.heading}")
    #     file.write(f"\n{indent}{'   ' if indent_level > 0 else ''} Level: {section.level}")
    #     file.write(f"\n{indent}{'   ' if indent_level > 0 else ''} Number of subsections: {len(section.subsections)}")
    #     parent_info = f"Parent: {parent_heading}" if parent_heading else "Parent: None (Root level)"
    #     file.write(f"\n{indent}{'   ' if indent_level > 0 else ''} {parent_info}")
        
    #     # Recursively write subsections
    #     for subsection in section.subsections:
    #         print_section_tree(subsection, file, indent_level + 1, section.heading)

    # # Calculate largest content length across all sections and subsections
    # largest_content = max(get_section_content_length(section) for section in sections)

    # # Create output file for section tree
    # output_file_path = "section_tree.txt"
    # print(f"\nWriting section tree to {output_file_path}...")

    # with open(output_file_path, "w", encoding="utf-8") as f:
    #     f.write(f"Document Section Tree Analysis\n")
    #     f.write(f"Found {len(sections)} top-level sections:\n")
    #     f.write(f"Largest content in chars: {largest_content}\n")
    #     f.write("=" * 80)
        
    #     for section in sections:
    #         print_section_tree(section, f)
    #         f.write(f"\n{'-' * 80}\n")

    # print(f"Section tree has been written to {output_file_path}")
    

if __name__ == "__main__":
    main()


