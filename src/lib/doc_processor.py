"""
Document processor module for handling .docx specification files.
Provides functionality to read and extract text content from 3GPP specification documents.
"""

from pathlib import Path
from typing import Dict, List, Generator
from docx import Document


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

        return doc

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def extract_paragraphs(doc: Document) -> Generator[Dict[str, str], None, None]:
    """
    Extract paragraphs from the document with their styles.

    Args:
        doc (Document): The loaded document object

    Returns:
        Dict containing:
            - text: The paragraph text
            - style: The paragraph style name
            - level: The heading level (if applicable)
    """
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

        yield {"text": para.text.strip(), "style": style_name, "level": level}


def extract_tables(doc: Document) -> Generator[List[List[str]], None, None]:
    """
    Extract tables from the document.

    Args:
        doc (Document): The loaded document object

    Returns:
        List[List[str]]: Each table as a list of rows, where each row is a list of cell texts
    """
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            if any(row_data):  # Only include rows that have some content
                table_data.append(row_data)
        if table_data:  # Only yield tables that have content
            yield table_data


def process_specification(file_path: str) -> None:
    """
    Process a specification document and print its content for review.

    Args:
        file_path (str): Path to the .docx file
    """
    try:
        doc = load_document(file_path)

        print(f"\nProcessing document: {file_path}")
        print("\n=== Paragraphs ===")
        for para in extract_paragraphs(doc):
            if para["level"] is not None:
                print(f"\nHeading Level {para['level']}:")
            print(f"Style: {para['style']}")
            print(f"Text: {para['text']}\n")

        print("\n=== Tables ===")
        for table in extract_tables(doc):
            print("\nNew Table:")
            for row in table:
                print(row)
            print()

    except Exception as e:
        print(f"Error processing document: {str(e)}")


if __name__ == "__main__":
    # Example usage
    data_dir = Path(__file__).parent.parent.parent / "data"

    # Process both specification files
    spec_files = ["23502-j20.docx", "24501.docx"]
    for spec_file in spec_files:
        file_path = data_dir / spec_file
        if file_path.exists():
            process_specification(str(file_path))
        else:
            print(f"Warning: Specification file not found: {spec_file}")
