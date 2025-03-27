import os
import time
import json
from docling.document_converter import DocumentConverter
import re
from chunker import create_chunks

def save_chunks_to_file(chunks, output_dir, filename):
    """
    Save chunks to a JSON file in a readable format
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{filename}_chunks.json")
    
    formatted_chunks = []
    for i, chunk in enumerate(chunks, 1):
        formatted_chunk = {
            "chunk_id": i,
            "title": chunk["title"],
            "content": chunk["content"] if isinstance(chunk["content"], str) else " ".join(chunk["content"]),
            "level": chunk["level"]
        }
        formatted_chunks.append(formatted_chunk)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(formatted_chunks, f, indent=2, ensure_ascii=False)
    
    print(f"→ Chunks saved to: {output_file}")
    # Also print first chunk as example
    if formatted_chunks:
        print("\nExample of first chunk:")
        print(json.dumps(formatted_chunks[0], indent=2))

def process_docx(docx_file: str, output_path: str, db_path: str):
    """
    Direct conversion from DOCX to processed markdown
    """
    total_start_time = time.time()
    print("\n=== Starting Document Processing ===")
    
    try:
        # Convert DOCX to markdown text
        print("\n[1/2] Converting DOCX to markdown...")
        converter = DocumentConverter()
        result = converter.convert(docx_file)
        markdown_text = result.document.export_to_markdown()
        
        # Process markdown content
        print("\n[2/2] Processing markdown content...")
        filtered_markdown = filter_markdown_content(markdown_text)
        
        # Write processed markdown
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(filtered_markdown)
            
        # Create chunks from the filtered markdown
        print("→ Creating chunks...")
        chunks = create_chunks(output_path, db_path)
        
        # Save chunks to processed_data directory
        filename = os.path.splitext(os.path.basename(docx_file))[0]
        processed_data_dir = os.path.join(os.path.dirname(os.path.dirname(output_path)), "processed_data")
        save_chunks_to_file(chunks, processed_data_dir, filename)
        
        total_duration = time.time() - total_start_time
        print(f"\n✓ All processing completed in {total_duration:.2f} seconds")
        return 0
        
    except Exception as e:
        print(f"\n✗ Processing failed: {e}")
        return 1

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

# Remove the last line if the heading is empty or contains only void
def _process_previous_heading(output_lines, current_heading, heading_content):
    if current_heading and (not heading_content or ''.join(heading_content).strip().lower() == "void"):
        output_lines.pop()

def clean_line(line):
    """Clean and normalize text lines"""
    line = re.sub(r'\[\d+\]', '', line)  # Remove reference numbers
    line = re.sub(r"[-/()[\]{}:,'\";?]", "", line)  # Remove punctuation
    line = re.sub(r"^\|+|\|+$", "", line)  # Remove table borders
    line = re.sub(r"^\s*\|", "", line)  # Remove leading table markers
    return re.sub(r"\s+", " ", line).strip()  # Normalize whitespace
