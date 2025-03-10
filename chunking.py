import re
from typing import Dict, List

def chunk_text_by_headings(text: str) -> List[Dict[str, str]]:
    """
    Chunks the document into sections based on heading levels (e.g., headings, subheadings, etc.) using numeric headings.
    
    Args:
        text (str): The cleaned text of the document.
        
    Returns:
        List[Dict[str, str]]: A list of dictionaries containing 'heading' and 'content' for each chunk.
    """
    # Regular expression to match headings with numbers (e.g., 5, 5.1, 5.1.1, etc.)
    heading_pattern = r'^\s*(\d+(\.\d+)*)(\s+.*)$'
    
    chunks = []
    current_chunk = None
    
    # Split the document by newlines
    lines = text.split('\n')
    
    for line in lines:
        heading_match = re.match(heading_pattern, line.strip())
        
        if heading_match:
            # If we already have a current chunk, save it first
            if current_chunk:
                chunks.append(current_chunk)
            
            # Extract the heading level and heading text
            heading_number = heading_match.group(1).strip()  # e.g., "5", "5.1", etc.
            heading_text = heading_match.group(3).strip()   # The text following the number (e.g., "Overview")
            
            # Determine the heading level based on the number of periods in the heading number
            heading_level = heading_number.count('.') + 1
            
            current_chunk = {'heading': heading_text, 'content': [], 'level': heading_level}
        
        elif current_chunk:
            # Add the line to the current chunk's content
            current_chunk['content'].append(line.strip())
    
    # Append the last chunk if exists
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def save_chunks_to_markdown(chunks: List[Dict[str, str]], output_file: str):
    """
    Saves the chunks into a markdown file.
    
    Args:
        chunks (List[Dict[str, str]]): The list of chunks to save.
        output_file (str): The file path where the chunks should be saved.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        for chunk in chunks:
            # Write the heading with the corresponding number of '#' symbols
            file.write(f"{'#' * chunk['level']} {chunk['heading']}\n")
            
            # Write the content under the heading
            for content_line in chunk['content']:
                file.write(f"{content_line}\n")
            
            file.write("\n" + "-" * 50 + "\n\n")  # Optional separator for clarity

# Example usage
with open("data/cleaned_TS_24.501.md", "r", encoding="utf-8") as file:
    text = file.read()

# Chunk the text by headings and subheadings
chunks = chunk_text_by_headings(text)

# Save the chunks to a markdown file
output_file_path = "data/chunked_output.md"
save_chunks_to_markdown(chunks, output_file_path)

print(f"Chunks saved to {output_file_path}")
