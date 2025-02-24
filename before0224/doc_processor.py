import sqlite3
import re
from docx import Document
from typing import List, Dict

# Create the database and table (make sure this is called once before storing any chunks)
def create_database(db_path: str):
    """
    Create the SQLite database and a table for storing document chunks.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS document_chunks (
                        chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chunk_text TEXT,
                        start_position INTEGER,
                        end_position INTEGER
                      )''')
    conn.commit()
    conn.close()


def store_chunk_in_db(db_path: str, chunk_text: str, start_position: int, end_position: int):
    """
    Store a chunk in the SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
        chunk_text (str): The chunk text to be stored.
        start_position (int): The starting position of the chunk in the document.
        end_position (int): The ending position of the chunk in the document.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the chunk into the database
    cursor.execute('''INSERT INTO document_chunks (chunk_text, start_position, end_position)
                      VALUES (?, ?, ?)''', (chunk_text, start_position, end_position))
    conn.commit()
    conn.close()


def generate_overlapping_chunks(doc, chunk_size=2000, overlap_ratio=0.1):
    """
    Generates overlapping chunks from the document text.

    Args:
        doc (Document): The loaded document object.
        chunk_size (int): The desired size of each chunk.
        overlap_ratio (float): The fraction of overlap between consecutive chunks.

    Returns:
        List of chunks, each of which is a string of text.
    """
    paragraphs = extract_paragraphs(doc)
    
    # Create a list to store chunks
    chunks = []
    
    # Calculate the overlap size
    overlap_size = int(chunk_size * overlap_ratio)
    
    # Flatten paragraphs into a single text string
    full_text = " ".join([para['text'] for para in paragraphs])
    
    # Split text into chunks with overlap
    for i in range(0, len(full_text), chunk_size - overlap_size):
        chunk = full_text[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks


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


def text_cleaner(text: str) -> str:
    """
    Clean and normalize text while preserving specific patterns and cases.

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
    text = re.sub(r'\b\d+\.\d+(?:\.\d+)*\b', lambda x: f"__{x.group(0)}__", text)
    
    # Remove punctuation marks only when they appear at the end of words
    text = re.sub(r'([.,!?:])\s', ' ', text)
    text = re.sub(r'([.,!?:])$', '', text)
    
    # Normalize whitespace by converting multiple spaces to a single one
    text = ' '.join(text.split())
    
    return text


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


def store_chunks_in_db(chunks, db_path="document_chunks.db"):
    """
    Store the document chunks in the SQLite database.

    Args:
        chunks (list): List of chunks to be stored in the database.
        db_path (str): Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert chunks into the database with positions
    for i, chunk in enumerate(chunks):
        start_position = i * (len(chunk) - len(chunk) // 10)  # Approximate start
        end_position = start_position + len(chunk)
        store_chunk_in_db(db_path, chunk, start_position, end_position)
    
    conn.close()


# Example usage:
docx_path = "data/24501-j11.docx"
doc = load_document(docx_path)

if doc:
    # Ensure the database is created before storing any chunks
    create_database("document_chunks.db")

    # Generate overlapping chunks and store them in the database
    chunks = generate_overlapping_chunks(doc, chunk_size=2000, overlap_ratio=0.1)

    # Store the chunks in the database
    store_chunks_in_db(chunks)

    # Print first few chunks for inspection
    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {i+1}:\n{chunk[:300]}...")  # Print first 300 characters
        print("-" * 40)
