"""
Document processor module for handling .docx specification files.
Provides functionality to read and extract text content from 3GPP specification documents.
"""

from pathlib import Path
import re
from typing import Dict, List, Optional
from docx import Document
from dataclasses import dataclass

@dataclass
class Section:
    """Represents a document section with its heading and content"""
    level: int
    heading: str
    content: List[Dict[str, str]]
    subsections: List['Section']
    parent: Optional['Section'] = None

def load_document(file_path: str) -> Document:
    """
    Load the document from the given file path.

    Args:
        file_path (str): Path to the .docx file

    Returns:
        Document: The loaded document object
    """
    try:
        print(f"Loading document from {file_path}")
        doc = Document(file_path)
        print(f"Document loaded successfully")
        return doc

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_paragraphs(doc: Document) -> List[Dict[str, any]]:
    """
    Extract paragraphs from the document with their styles.

    Args:
        doc (Document): The loaded document object

    Returns:
        List[Dict]: List of paragraphs, each containing:
            - text: The paragraph text
            - style: The paragraph style name
            - level: The heading level (if applicable)
    """
    paragraphs = []
    for para in doc.paragraphs:
        if not para.text.strip():  # Skip empty paragraphs
            continue

        # Get paragraph style information
        style_name = para.style.name if para.style else "Normal"
        level = None

        # Check if it's a heading and get its level
        if style_name.startswith("Heading"):
            try:
                level = int(style_name.split()[-1])
            except (ValueError, IndexError):
                pass


        
        paragraphs.append({
            "text": text_cleaner(para.text),
            "style": text_cleaner(style_name),
            "level": level
        })
    
    return paragraphs

def extract_section_tree(doc: Document, max_heading_level: int = 4) -> List[Section]:
    """
    Extract document content as a tree of sections based on heading hierarchy.
    This allows for processing the document in meaningful chunks based on its structure.

    Args:
        doc (Document): The loaded document object
        max_heading_level (int): Maximum heading level to consider for sectioning

    Returns:
        List[Section]: List of top-level sections, each containing their subsections
    """
    print("Extracting section tree")
    if doc is None:
        print("Document is None!")
        return []

    current_sections = [None] * (max_heading_level + 1)  # Track current section at each level
    current_content = []
    top_level_sections = []  # Store all level 1 sections
    max_chunk_size = 2000
    
    paragraphs = extract_paragraphs(doc)
    
    for para in paragraphs:
        level = para.get("level")
        
        if level is not None and level <= max_heading_level and para["text"][0].isdigit():
            # We found a heading, create a new section
            new_section = Section(
                level=level,
                heading=para["text"].strip().replace(" ", "_"),
                content=[],
                subsections=[],
                parent=current_sections[level - 1] if level > 0 else None
            )
            
            # Add accumulated content to the previous section at this level if it exists
            if current_sections[level] is not None:
                current_sections[level].content.extend(current_content)
            
            # Update the section hierarchy
            if level > 0 and current_sections[level - 1] is not None:
                current_sections[level - 1].subsections.append(new_section)
            
            current_sections[level] = new_section
            current_content = []
            
            # Clear all lower level sections
            for i in range(level + 1, max_heading_level + 1):
                current_sections[i] = None
                
            if level == 1:
                top_level_sections.append(new_section)
        else:
            # Accumulate content for the current lowest-level section
            if current_content and len(current_content[-1]) + len(para["text"]) < max_chunk_size and para.get("level") is None:
                # Combine with previous text if conditions are met
                current_content[-1] = current_content[-1] + " " + para["text"]
            else:
                current_content.append(para["text"])
    
    # Add any remaining content to the last section
    for level in range(max_heading_level, 0, -1):
        if current_sections[level] is not None:
            current_sections[level].content.extend(current_content)
            break
    
    return top_level_sections


def text_cleaner(text: str) -> str:
    """
    Clean and normalize text while preserving specific patterns and cases.
    
    The function performs the following operations:
    1. Replaces non-breaking spaces and tabs with regular spaces
    2. Preserves version numbers (e.g., 1.2, 5.5.1.2)
    3. Removes punctuation marks (.,!?:) when they appear at the end of words
    4. Normalizes whitespace
    5. Performs case normalization with specific preservation rules:
        - Preserves words containing numbers (e.g., "5G")
        - Preserves words with multiple uppercase letters (e.g., "IP", "NSSAI")
        - Preserves words containing special characters (e.g., "S-NSSAI(s)")
        - Converts all other words to lowercase
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned and normalized text with preserved patterns
    """
    if not text:
        return ""
        
    # Replace non-breaking spaces and tabs with regular spaces
    text = text.replace("\xa0", " ").replace("\t", " ")
    
    # Preserve version numbers (e.g., 1.2, 5.5.1.2)
    # This pattern matches two or more numbers separated by dots
    text = re.sub(r'\b\d+\.\d+(?:\.\d+)*\b', lambda x: f"__{x.group(0)}__", text)
    
    # Remove punctuation marks only when they appear at the end of words
    text = re.sub(r'([.,!?:])\s', ' ', text)
    text = re.sub(r'([.,!?:])$', '', text)
    
    text = text.replace("__", "")

    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Process each word for case normalization
    words = text.split()
    normalized_words = []
    for word in words:
        # Preserve if:
        # 1. Contains numbers
        # 2. Contains more than one uppercase letter
        # 3. Contains special characters (excluding common punctuation)
        if (any(c.isdigit() for c in word) or  # Has numbers
            sum(1 for c in word if c.isupper()) > 1 or  # Multiple uppercase
            any(c for c in word if not c.isalnum())):  # Has symbols
            normalized_words.append(word)
        else:
            normalized_words.append(word.lower())
    
    return ' '.join(normalized_words)


def remove_sections(file_path: str, excluded_sections: List[str]) -> str:
    """
    Remove specified sections from a document and save the stripped version.

    Args:
        file_path (str): Path to the source document
        excluded_sections (List[str]): List of section names to remove from the document

    Returns:
        str: Path to the saved stripped document in the data/stripped directory

    This function removes all paragraphs that are part of the excluded sections and
    saves the resulting document with the same name in the data/stripped directory.
    """
    doc = load_document(file_path)

    remove = True
    for para in doc.paragraphs:
        para.text = text_cleaner(para.text)
        if para.style.name.startswith("Heading") and any(word in para.text.lower() for word in excluded_sections):
            remove = True

        elif para.style.name.startswith("Heading") and remove:
            remove = False
        if remove:
            para.clear()
            p = para._element
            p.getparent().remove(p)

    # Extract original filename and save stripped version
    doc_name = Path(file_path).name
    save_path = f"data/stripped/{doc_name}"
    doc.save(save_path)
    return save_path
        