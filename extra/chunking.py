"""
Document processor module for handling .pdf specification files.
Provides functionality to read and extract text content from 3GPP specification documents.
"""

from pathlib import Path
import re
from typing import Dict, List, Optional
import fitz  # PyMuPDF
from dataclasses import dataclass
import os

@dataclass
class Section:
    """Represents a document section with its heading and content"""

    level: int
    heading: str
    content: List[str]
    subsections: List["Section"]
    parent: Optional["Section"] = None

def load_document(file_path: str) -> fitz.Document:
    """
    Load the document from the given file path.

    Args:
        file_path (str): Path to the .pdf file

    Returns:
        fitz.Document: The loaded document object
    """
    try:
        print(f"Loading document from {file_path}")
        doc = fitz.open("data/TS 24.501.pdf")
        print("Document loaded successfully")
        return doc

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_paragraphs(doc: fitz.Document) -> List[Dict[str, any]]:
    """
    Extract paragraphs from the document with their styles (approximated).

    Args:
        doc (fitz.Document): The loaded document object

    Returns:
        List[Dict]: List of paragraphs, each containing:
            - text: The paragraph text
            - style: Approximated paragraph style (e.g., "Heading 1", "Normal")
            - level: Approximated heading level (if applicable)
    """
    paragraphs = []
    for page in doc:
        text_blocks = page.get_text("dict", flags=0)["blocks"]
        for block in text_blocks:
            if block["type"] == 0:  # Text block
                lines = block["lines"]
                for line in lines:
                    spans = line["spans"]
                    paragraph_text = "".join(span["text"] for span in spans)
                    if not paragraph_text.strip():
                        continue

                    # Approximate heading level based on font size and position
                    level = None
                    style_name = "Normal"
                    if spans:
                        font_size = spans[0]["size"]
                        if font_size > 14:  # Adjust threshold as needed
                            style_name = "Heading 1"
                            level = 1
                        elif font_size > 12:
                            style_name = "Heading 2"
                            level = 2
                        elif font_size > 10:
                            style_name = "Heading 3"
                            level = 3

                    paragraphs.append(
                        {
                            "text": text_cleaner(paragraph_text),
                            "style": text_cleaner(style_name),
                            "level": level,
                        }
                    )

    return paragraphs

def extract_section_tree(doc: fitz.Document, max_heading_level: int = 8) -> List[Section]:
    """
    Extract document content as a tree of sections based on heading hierarchy.
    This allows for processing the document in meaningful chunks based on its structure.

    Args:
        doc (fitz.Document): The loaded document object
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
    max_chunk_size = 2000

    paragraphs = extract_paragraphs(doc)

    for para in paragraphs:
        level = para.get("level")

        if level is not None and level <= max_heading_level and para["text"][0].isdigit():
            new_section = Section(
                level=level,
                heading=para["text"].strip().replace(" ", "_"),
                content=[],
                subsections=[],
                parent=current_sections[level - 1] if level > 1 else None,
            )

            deepest_section = None
            for i in range(max_heading_level, 0, -1):
                if current_sections[i] is not None:
                    deepest_section = current_sections[i]
                    break
            if deepest_section is not None:
                deepest_section.content.extend(current_content)

            if level > 1 and current_sections[level - 1] is not None:
                current_sections[level - 1].subsections.append(new_section)

            current_sections[level] = new_section
            current_content = []

            for i in range(level + 1, max_heading_level + 1):
                current_sections[i] = None

            if level == 1:
                top_level_sections.append(new_section)
        else:
            if (
                current_content
                and len(current_content[-1]) + len(para["text"]) < max_chunk_size
                and para.get("level") is None
            ):
                current_content[-1] = current_content[-1] + " " + para["text"]
            else:
                current_content.append(para["text"])

    deepest_section = None
    for i in range(max_heading_level, 0, -1):
        if current_sections[i] is not None:
            deepest_section = current_sections[i]
            break
    if deepest_section is not None:
        deepest_section.content.extend(current_content)

    return top_level_sections

def text_cleaner(text: str) -> str:
    # (Same as before)
    if not text:
        return ""

    text = text.replace("\xa0", " ").replace("\t", " ")
    text = re.sub(r"\b\d+\.\d+(?:\.\d+)*\b", lambda x: f"__{x.group(0)}__", text)
    text = re.sub(r"([.,!?:])\s", " ", text)
    text = re.sub(r"([.,!?:])$", "", text)
    text = text.replace("__", "")
    text = " ".join(text.split())

    words = text.split()
    normalized_words = []
    for word in words:
        if (
            any(c.isdigit() for c in word)
            or sum(1 for c in word if c.isupper()) > 1
            or any(c for c in word if not c.isalnum())
        ):
            normalized_words.append(word)
        else:
            normalized_words.append(word.lower())

    return " ".join(normalized_words)

# Create necessary directories
def ensure_directories_exist():
    """Create necessary directories if they don't exist."""
    directories = [
        "data/stripped",
        "processed_data"
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def remove_sections(file_path: str, excluded_sections: List[str]) -> str:
    """Remove specified sections from the PDF text."""
    # Create directories before processing
    ensure_directories_exist()
    
    doc = load_document(file_path)
    if doc is None:
        return ""

    remove = False
    new_paragraphs = []
    for page in doc:
        text_blocks = page.get_text("dict", flags=0)["blocks"]
        for block in text_blocks:
            if block["type"] == 0:
                lines = block["lines"]
                for line in lines:
                    spans = line["spans"]
                    paragraph_text = "".join(span["text"] for span in spans)
                    paragraph_text = text_cleaner(paragraph_text)
                    if not paragraph_text.strip():
                        continue

                    if paragraph_text.lower().startswith(tuple(word.lower() for word in excluded_sections)) or not paragraph_text.strip()[0].isdigit() and any(word.lower() in paragraph_text.lower() for word in excluded_sections):
                        print(f"Removing section: {paragraph_text}")
                        remove = True
                    elif paragraph_text.lower().startswith("chapter") and remove:
                        remove = False
                    if not remove:
                        new_paragraphs.append(paragraph_text)

    output_text = "\n\n".join(new_paragraphs)
    doc_name = Path(file_path).name
    save_path = os.path.join("data", "stripped", os.path.basename(file_path))
    with open(save_path.replace(".pdf", ".txt"), "w", encoding='utf-8') as f:
        f.write(output_text)
    return save_path.replace(".pdf", ".txt")

def save_sections_to_markdown(sections: List[Section], output_file: str = "output.md"):
    """
    Saves the section tree to a markdown file.

    Args:
        sections (List[Section]): List of top-level sections
        output_file (str): Path to the output markdown file
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for section in sections:
            _write_section_to_markdown(section, f)

def _write_section_to_markdown(section: Section, file):
    """Recursively writes a section and its subsections to a markdown file."""
    file.write(f"{'#' * section.level} {section.heading.replace('_', ' ')}\n\n")

    for content in section.content:
        file.write(f"{content}\n\n")

    for subsection in section.subsections:
        _write_section_to_markdown(subsection, file)
    file.write("---\n\n")

if __name__ == "__main__":
    # Ensure directories exist before processing
    ensure_directories_exist()
    
    pdf_file_path = "data/TS 24.501.pdf"  # Replace with your PDF file path
    excluded_sections = ["References", "Change history"] # Add any section to remove.

    # Remove excluded sections and get the path to the stripped document
    stripped_pdf_path = remove_sections(pdf_file_path, excluded_sections)

    if stripped_pdf_path:
        doc = load_document(pdf_file_path) # load the original document, not the stripped one.
        if doc:
            sections = extract_section_tree(doc)
            save_sections_to_markdown(sections)
            print("Sections saved to output.md")
        else:
            print("Failed to load document.")
    else:
        print("Failed to remove sections.")