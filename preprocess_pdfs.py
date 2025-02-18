import os
import logging
import json
import hashlib
from typing import List, Dict
from pypdf import PdfReader
import re
from rich.console import Console
from rich.logging import RichHandler
from tqdm import tqdm

# Set up rich console logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)

DOCS_CACHE_FILE = "raw_docs_cache.json"

def get_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    file_path = os.path.normpath(file_path)
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_docs_cache() -> Dict:
    """Load raw documents from cache"""
    if os.path.exists(DOCS_CACHE_FILE):
        try:
            with open(DOCS_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load docs cache file: {str(e)}[/yellow]")
    return {}

def save_docs_cache(cache: Dict):
    """Save raw documents to cache"""
    try:
        with open(DOCS_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not save docs cache file: {str(e)}[/yellow]")

def clean_text(text: str) -> str:
    """Cleans extracted text by removing noise, ToC, and normalizing content."""
    try:
        # Ensure text is a string
        if text is None:
            return ""  # Return empty string if text is None
        
        if not isinstance(text, str):
            text = str(text)  # Convert to string if it's not already
        
        # Remove common PDF artifacts
        text = re.sub(r'\bPage\s+\d+\s+of\s+\d+\b', '', text)  # Remove "Page X of Y"
        text = re.sub(r'\f', '\n', text)  # Replace form feeds with newlines
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines with spaces

        # Remove 3GPP document headers and footers
        text = re.sub(r'(?m)^3GPP TS \d+\.\d+.*$', '', text)  # Remove TS headers
        text = re.sub(r'(?m)^3GPP TR \d+\.\d+.*$', '', text)  # Remove TR headers
        text = re.sub(r'(?m)^Release \d+.*$', '', text)  # Remove Release info
        text = re.sub(r'ETSI\s+\d+\s+\d+\s+V\d+\.\d+\.\d+.*$', '', text, flags=re.MULTILINE)

        # Remove Table of Contents (ToC) based on common patterns
        text = re.sub(r'(?m)^\s*\d+(\.\d+)*\s+.*?\.{3,}\s*\d+\s*$', '', text)  # Matches "1.2 Section Name .... 5"
        text = re.sub(r'(?m)^\s*[IVXLCDM]+\.\s+.*?\.{3,}\s*\d+\s*$', '', text)  # Matches "III. Some Title .... 12"
        text = re.sub(r'(?m)^\s*Chapter\s+\d+\s+.*?\.{3,}\s*\d+\s*$', '', text)  # Matches "Chapter 3 ... 45"
        text = re.sub(r'(?m)^\s*\d+\s+[A-Za-z].*?\.{3,}\s*\d+\s*$', '', text)  # Matches "5 Introduction ... 3"

        # Remove very short lines (likely artifacts)
        lines = [line for line in text.split('\n') if len(line.strip()) > 5]
        text = '\n'.join(lines)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = re.sub(r'\n\s*\n+', '\n\n', text)  # Normalize paragraph breaks
        
        return text.strip()
    except Exception as e:
        logging.warning(f"Error in clean_text: {str(e)}")
        return ""

def is_section_heading(line: str) -> bool:
    """Check if a line is a section heading."""
    # Common 3GPP section heading patterns
    heading_patterns = [
        r'^\d+(?:\.\d+)*\s+[A-Z]',  # Numbered sections (e.g., "4.1 Overview")
        r'^Annex [A-Z]',  # Annexes
        r'^Table \d+[\-\.]?\d*',  # Tables with possible subsections
        r'^Figure \d+[\-\.]?\d*',  # Figures with possible subsections
        r'^[A-Z][A-Za-z\s]+$',  # All caps or Title Case headings
    ]
    
    line = line.strip()
    return any(re.match(pattern, line) for pattern in heading_patterns) and len(line) < 100

def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into meaningful chunks based on 3GPP document structure."""
    chunks = []
    current_chunk = []
    current_heading = None
    current_size = 0
    
    # Split into lines while preserving paragraph structure
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if is_section_heading(line):
            # Save previous chunk if it exists
            if current_chunk and current_size > 50:  # Minimum chunk size
                chunk_text = '\n'.join(current_chunk)
                if current_heading:
                    chunk_text = f"{current_heading}\n{chunk_text}"
                chunks.append(chunk_text)
            
            current_heading = line
            current_chunk = []
            current_size = 0
        else:
            current_chunk.append(line)
            current_size += len(line)
            
            # Split if chunk is too large, but try to break at paragraph boundaries
            if current_size > max_chunk_size:
                chunk_text = '\n'.join(current_chunk)
                if current_heading:
                    chunk_text = f"{current_heading}\n{chunk_text}"
                chunks.append(chunk_text)
                current_chunk = []
                current_size = 0
    
    # Add the last chunk if it's substantial
    if current_chunk and current_size > 50:
        chunk_text = '\n'.join(current_chunk)
        if current_heading:
            chunk_text = f"{current_heading}\n{chunk_text}"
        chunks.append(chunk_text)
    
    return chunks

def read_pdfs_from_directory(data_dir: str) -> List[Dict[str, str]]:
    """Read PDF files from the specified directory and return a list of documents with extracted text."""
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(data_dir, filename)
            try:
                with open(file_path, "rb") as f:
                    reader = PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    
                    # Clean and chunk the text if necessary
                    cleaned_text = clean_text(text)
                    documents.append({"filename": filename, "text": cleaned_text})
                    console.print(f"[green]✅ Successfully extracted text from {filename}[/green]")
            except Exception as e:
                console.print(f"[red]❌ Error reading {filename}: {str(e)}[/red]")
    
    return documents

if __name__ == "__main__":
    try:
        console.print("[bold blue]Starting PDF preprocessing...[/bold blue]")
        data_directory = "data"
        documents = read_pdfs_from_directory(data_directory)
        console.print(f"[bold green]✅ Successfully processed {len(documents)} documents[/bold green]")
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
