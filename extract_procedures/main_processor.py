"""
Document processor module for handling .docx specification files.
Provides functionality to read and extract text content from 3GPP specification documents.
"""

from pathlib import Path
import re
from typing import Dict, List, Optional
from docx import Document
from dataclasses import dataclass
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
        if not para.text.strip():  
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

    current_sections = [None] * (max_heading_level + 1) 
    current_content = []
    top_level_sections = [] 
    excluded_section = ["scope", "references", "abbreviations", ]
    
    paragraphs = extract_paragraphs(doc)
    
    for para in paragraphs:
        level = para.get("level")
        
        if level is not None and level <= max_heading_level and para["text"][0].isdigit() and all(word not in para["text"].lower() for word in excluded_section):
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
            if current_content and len(current_content[-1]) + len(para["text"]) < 3000 and para.get("level") is None:
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
        if (any(c.isdigit() for c in word) or  
            sum(1 for c in word if c.isupper()) > 1 or  
            any(c for c in word if not c.isalnum())):  
            normalized_words.append(word)
        else:
            normalized_words.append(word.lower())
    
    return ' '.join(normalized_words)

def create_chunks_with_context(sections: List[Section]) -> List[Dict[str, any]]:
    """Creates chunks with contextual information (using LangChain's RecursiveCharacterTextSplitter)."""

    all_text = ""
    for section in sections:
        section_text = ""
        for item in section.content:
            section_text += item + " "
        all_text += section_text + "\n\n" 

        # Recursively add sub-sections
        for subsection in section.subsections:
            subsection_text = ""
            for item in subsection.content:
                subsection_text += item + " "
            all_text += subsection_text + "\n\n" 

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""] 
    )
    docs = text_splitter.create_documents([all_text]) 

    chunks = []
    for i, doc in enumerate(docs):
        chunks.append({
            "chunk_id": f"chunk_{i}",
            "chunk_content": doc.page_content 
        })

    return chunks

def extract_nas_nr_data(text: str, target_procedure: str) -> Dict[str, any]:
    """Extract nodes and edges related to a specific NAS NR procedure from a given text chunk."""
    nodes = {}
    edges = []

    if target_procedure.lower() in text.lower(): 
        for entity_match in re.finditer(r"\b[A-Za-z]+(?:[\s-][A-Za-z]+)*\b", text):
            entity_name = entity_match.group(0).strip()
            if entity_name not in nodes:
                nodes[entity_name] = {"label": "Entity", "properties": {}}

                # Property extraction (improved regex)
                property_matches = re.finditer(r"(\w+)\s*:\s*([^.,;]+)", text)
                for prop_match in property_matches:
                    key = prop_match.group(1).strip()
                    value = prop_match.group(2).strip()
                    nodes[entity_name]["properties"][key] = value

        for rel_match in re.finditer(r"(\b[A-Za-z]+(?:[\s-][A-Za-z]+)*\b)\s+(?:is related to|depends on|requires|connected to|sends|receives|uses|supports|configures|associated with)\s+(\b[A-Za-z]+(?:[\s-][A-Za-z]+)*\b)", text):
            source = rel_match.group(1).strip()
            target = rel_match.group(2).strip()
            relation_type = rel_match.group(0).strip().split()[1] 

            if source in nodes and target in nodes:
                edges.append({
                    "source": source,
                    "target": target,
                    "type": relation_type,
                    "properties": {}  
                })

    return {"nodes": nodes, "edges": edges}


def process_chunks_and_extract_graph(chunks: List[Dict[str, any]], target_procedure: str) -> Dict[str, any]:
    """Processes chunks and extracts graph data for the target procedure."""

    all_nodes = {}
    all_edges = []

    for chunk in chunks:
        chunk_text = chunk["chunk_content"]
        extracted_data = extract_nas_nr_data(chunk_text, target_procedure)  

        for node_id, node_data in extracted_data["nodes"].items():
            if node_id not in all_nodes: 
                all_nodes[node_id] = node_data

        all_edges.extend(extracted_data["edges"])

    nodes_list = [{"id": identifier, "label": data["label"], "properties": data["properties"]} for identifier, data in all_nodes.items()]

    return {"nodes": nodes_list, "edges": all_edges}
    
    
