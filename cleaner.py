import re
from typing import Dict, List, Tuple
import os

def clean_text(text: str) -> str:
    """Cleans extracted PDF text by removing TOC, headers, footers, images, and page numbers.
    
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
    with open("data/TS_24.501.md", "r", encoding="utf-8") as file:
        text = file.read()  # Read the entire file as a single string
    processed_text = clean_text(text)  # Use the clean_text function
    with open("data/cleaned_TS_24.501.md", "w", encoding="utf-8") as file:
        file.write(processed_text)
