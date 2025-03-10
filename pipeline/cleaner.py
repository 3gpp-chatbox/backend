import re
from typing import Dict, List, Tuple
import os
from pathlib import Path

def clean_text(text: str) -> str:
    """Cleans extracted PDF text by removing headers, footers, images, and page numbers.
    
    Args:
        text (str): Raw text extracted from PDF
        
    Returns:
        str: Cleaned text
    """
   
    
    # Remove specific headers like document title and version (e.g., "3GPP TS 24.501 version 18.9.0 Release 18")
    header_patterns = [
        r'^\s*3GPP TS 24\.501.*?Release \d+.*$',  # Matches headers like "3GPP TS 24.501 version 18.9.0 Release 18"
        r'^\s*ETSI TS 124 501.*?V\d+\.\d+\.\d+.*$',  # Matches "ETSI TS 124 501 V18.9.0 (2025-01)"
    ]
    for pattern in header_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    
    # Remove footer patterns like 'ETSI' or other footer content
    footer_patterns = [
        r'\bETSI\b',  # Matches the standalone "ETSI" string
        r'\bPage \d+\b',  # Matches "Page X" (page numbers)
        r'(?<=\n)\d+\s*\n',  # Matches page numbers after newlines (e.g., "1\n", "2\n")
    ]
    for pattern in footer_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    
    # Remove image placeholders or references (optional, depends on how images are represented in the text)
    text = re.sub(r'\[image\]', '', text)  # Remove image placeholders
    
    # Remove extra blank lines (headers, footers may leave extra lines)
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove empty or whitespace-only lines
    
    return text

if __name__ == "__main__":
    # Get the backend directory path (two levels up from this script)
    backend_dir = Path(__file__).parent.parent
    
    # Define input and output paths relative to backend directory
    input_markdown = str(backend_dir / "processed_data" / "TS_24.501.md")
    output_markdown = str(backend_dir / "processed_data" / "cleaned_TS_24.501.md")
    
    print(f"Reading markdown from: {input_markdown}")
    print(f"Saving cleaned markdown to: {output_markdown}")
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_markdown), exist_ok=True)
    
    # Process the file
    with open(input_markdown, "r", encoding="utf-8") as file:
        text = file.read()
    processed_text = clean_text(text)
    with open(output_markdown, "w", encoding="utf-8") as file:
        file.write(processed_text)
        
    print("Cleaning completed successfully!")
