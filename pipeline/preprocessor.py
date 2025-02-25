import os
import time
from docling.document_converter import DocumentConverter
import re
from chunker import create_chunks
from db_handler import DBHandler

def docx_to_markdown_with_docling(docx_file, md_file):
    start_time = time.time()
    print("\n[1/2] Starting Docling conversion...")
    try:
        converter = DocumentConverter()
        result = converter.convert(docx_file)
        markdown_text = result.document.export_to_markdown()
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        duration = time.time() - start_time
        print(f"\u2713 Markdown file created: {md_file}")
        print(f"\u2713 Conversion completed in {duration:.2f} seconds")
        return 0
    except Exception as e:
        print(f"\u2717 Error during conversion: {e}")
        return 1

def process_markdown(input_path: str, output_path: str, db_path: str):
    start_time = time.time()
    print("\n[2/2] Starting Markdown processing...")
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        with open(input_path, "r", encoding="utf-8") as f:
            markdown_text = f.read()      
        
        print("→ Filtering content...")
        filtered_markdown = filter_markdown_content(markdown_text)       
        
        # Only write to output file if it's different from input
        if input_path != output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(filtered_markdown)
        
        # Create chunks from the filtered markdown
        print("→ Creating chunks...")
        chunks = create_chunks(output_path, db_path)
        
        duration = time.time() - start_time
        print(f"✓ Processing completed in {duration:.2f} seconds")    
    except Exception as e:
        print(f"✗ Error: {e}")

def filter_markdown_content(markdown_text):
    lines = markdown_text.splitlines()
    output_lines = []
    exclude_content = False
    in_table = False
    found_first_heading = False
    
    exclude_keywords = ["Forward", "Scope", "References", "Definitions", 
                        "Abbreviations", "Annex", "Table of Contents"]
    
    current_heading = None
    heading_content = []
    
    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else None
        line = line.strip()
        
        if not found_first_heading:
            if line.startswith('#'):
                found_first_heading = True
            else:
                continue
        
        if _is_table_line(line):
            in_table = True
            continue
        elif in_table and not line:
            in_table = False
            continue
        elif in_table:
            continue
        
        if line.startswith('#'):
            _process_previous_heading(output_lines, current_heading, heading_content)
            
            heading_text = line.strip('#').strip()
            if any(keyword.lower() in heading_text.lower() for keyword in exclude_keywords):
                exclude_content = True
                current_heading = None
                heading_content = []
                continue
            else:
                exclude_content = False
                output_lines.append(line)
                current_heading = line
                heading_content = []
        else:
            if not exclude_content:
                cleaned_line = clean_line(line)
                if cleaned_line:
                    output_lines.append(cleaned_line)
                    heading_content.append(cleaned_line)
    
    _process_previous_heading(output_lines, current_heading, heading_content)
    return '\n'.join(output_lines)

def _is_table_line(line):
    return line.startswith('|') or (line and all(c == '-' or c == '|' for c in line))

def _process_previous_heading(output_lines, current_heading, heading_content):
    if current_heading and (not heading_content or ''.join(heading_content).strip().lower() == "void"):
        output_lines.pop()

def clean_line(line):
    line = re.sub(r'\[\d+\]', '', line)
    line = re.sub(r"[-/()[\]{}:,'\";?]", "", line)
    line = re.sub(r"^\|+|\|+$", "", line)
    line = re.sub(r"^\s*\|", "", line)
    return re.sub(r"\s+", " ", line).strip()
