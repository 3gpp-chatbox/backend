"""
Document processor module for handling .docx specification files.
Provides functionality to read and extract text content from 3GPP specification documents.
"""

from pathlib import Path
import re
from typing import Dict, List, Optional
from docx import Document
from dataclasses import dataclass
from collections import defaultdict

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

def extract_tables(doc: Document) -> List[List[List[str]]]:
    """
    Extract tables from the document.

    Args:
        doc (Document): The loaded document object

    Returns:
        List[List[List[str]]]: List of tables, where each table is a list of rows,
                              and each row is a list of cell texts
    """
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            if any(row_data):  # Only include rows that have some content
                table_data.append(row_data)
        if table_data:  # Only include tables that have content
            tables.append(table_data)
    return tables

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
    
    paragraphs = extract_paragraphs(doc)
    
    for para in paragraphs:
        level = para.get("level")
        
        if level is not None and level <= max_heading_level:
            # We found a heading, create a new section
            new_section = Section(
                level=level,
                heading=para["text"].strip(),
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
            current_content.append(para["text"])
    
    # Add any remaining content to the last section
    for level in range(max_heading_level, 0, -1):
        if current_sections[level] is not None:
            current_sections[level].content.extend(current_content)
            break
    
    return top_level_sections

def extract_procedure_sections(doc: Document) -> List[Dict]:
    """
    Extract sections that likely contain procedure descriptions.
    This is specifically designed for 3GPP specifications where procedures
    are typically described in sections with specific heading patterns.

    Args:
        doc (Document): The loaded document object

    Returns:
        List[Dict]: List of procedure sections, each containing:
            - heading: The procedure section heading
            - content: The procedure content
            - level: The heading level
            - subsections: List of subsections
    """
    procedure_keywords = [
        "procedure", "procedures", "flow", "flows", "message flow",
        "call flow", "signalling flow", "operation", "operations"
    ]
    
    procedure_sections = []
    sections = extract_section_tree(doc)
    
    for section in sections:
        if any(keyword in section.heading.lower() for keyword in procedure_keywords):
            procedure_sections.append({
                "heading": section.heading,
                "content": section.content,
                "level": section.level,
                "subsections": section.subsections
            })
    
    return procedure_sections

def process_procedures_in_chunks(file_path: str) -> List[Dict]:
    """
    Process a 3GPP specification document focusing on procedures.

    Args:
        file_path (str): Path to the .docx file

    Returns:
        List[Dict]: List of procedure information suitable for graph creation
    """
    try:
        doc = load_document(file_path)
        if not doc:
            return []

        procedures = extract_procedure_sections(doc)
        return procedures

    except Exception as e:
        print(f"Error processing procedures: {str(e)}")
        return []

def process_specification(file_path: str) -> None:
    """
    Process a specification document and print its content for review.

    Args:
        file_path (str): Path to the .docx file
    """
    try:
        doc = load_document(file_path)
        if not doc:
            return

        print(f"\nProcessing document: {file_path}")
        
        print("\n=== Paragraphs ===")
        paragraphs = extract_paragraphs(doc)
        for para in paragraphs:
            if para["level"] is not None:
                print(f"\nHeading Level {para['level']}:")
            print(f"Style: {para['style']}")
            print(f"Text: {para['text']}\n")

        print("\n=== Tables ===")
        tables = extract_tables(doc)
        for table in tables:
            print("\nNew Table:")
            for row in table:
                print(row)
            print()

    except Exception as e:
        print(f"Error processing document: {str(e)}")



def text_cleaner(text: str) -> str:
    """
    Clean and normalize text while preserving 3GPP-specific patterns.
    Handles:
    - Version numbers (e.g., 1.2, 5.5.1.2, 3.2.433, 15.4.0)
    - Technical terms with special characters (e.g., s-nssai(s))
    - Non-breaking spaces and tabs
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return ""
        
    # Replace non-breaking spaces and tabs with regular spaces
    text = text.replace("\xa0", " ").replace("\t", " ")
    
    # Preserve version numbers (e.g., 1.2, 5.5.1.2)
    # This pattern matches two or more numbers separated by dots
    text = re.sub(r'\b\d+\.\d+(?:\.\d+)*\b', lambda x: f"__{x.group(0)}__", text)
    
    return text
    # # Preserve technical terms with hyphens and parentheses
    # # e.g., s-nssai(s), n1-mode, amf-ue-ngap-id
    # text = re.sub(r'[a-zA-Z0-9]+(?:[-][a-zA-Z0-9]+)*(?:\([a-zA-Z]+\))?',
    #               lambda x: f"__{x.group(0)}__", text)
    
    # # Remove other special characters but keep the preserved patterns
    # text = ''.join([char if char.isalnum() or char.isspace() or char == '__' 
    #                 else ' ' for char in text])
    
    # # Restore preserved patterns
    # text = text.replace("__", "")
    
    # # Normalize whitespace
    # text = ' '.join(text.split())
    
    # # Convert to lowercase but preserve acronyms of 2-5 characters
    # words = text.split()
    # normalized_words = []
    # for word in words:
    #     if word.isupper() and 2 <= len(word) <= 5:
    #         normalized_words.append(word)  # Keep acronyms as is
    #     else:
    #         normalized_words.append(word.lower())
    
    # return ' '.join(normalized_words)


