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
    """Cleans extracted text by removing noise and normalizing content."""
    try:
        # Handle potential encoding issues
        if not isinstance(text, str):
            text = str(text, errors='ignore')
        
        # Remove common PDF artifacts
        text = re.sub(r'\bPage\s+\d+\s+of\s+\d+\b', '', text)  # Remove "Page X of Y"
        text = re.sub(r'\f', '\n', text)  # Replace form feeds with newlines
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines with spaces
        
        # Remove 3GPP document headers and footers
        text = re.sub(r'(?m)^3GPP TS \d+\.\d+.*$', '', text)  # Remove TS headers
        text = re.sub(r'(?m)^3GPP TR \d+\.\d+.*$', '', text)  # Remove TR headers
        text = re.sub(r'(?m)^Release \d+.*$', '', text)  # Remove Release info
        text = re.sub(r'ETSI\s+\d+\s+\d+\s+V\d+\.\d+\.\d+.*$', '', text, flags=re.MULTILINE)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = re.sub(r'\n\s*\n+', '\n\n', text)  # Normalize paragraph breaks
        
        # Remove very short lines (likely artifacts)
        lines = [line for line in text.split('\n') if len(line.strip()) > 5]
        text = '\n'.join(lines)
        
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

def read_pdfs_from_directory(directory: str) -> List[Dict[str, str]]:
    """Read and preprocess PDFs from a directory with caching"""
    documents = []
    cache = load_docs_cache()
    
    if not os.path.exists(directory):
        error_msg = f"Directory {directory} not found"
        console.print(f"[red]{error_msg}[/red]")
        raise FileNotFoundError(error_msg)
    
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        console.print(f"[yellow]Warning: No PDF files found in {directory}[/yellow]")
        return documents
    
    console.print(f"[bold green]Found {len(pdf_files)} PDF files to process[/bold green]")
    
    # Process each PDF with progress bar
    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        file_path = os.path.join(directory, filename)
        
        # Check if file is in cache and hash matches
        file_hash = get_file_hash(file_path)
        if file_path in cache and cache[file_path]["hash"] == file_hash:
            console.print(f"[green]Using cached content for {filename}[/green]")
            documents.append(cache[file_path]["data"])
            continue
        
        console.print(f"[blue]Processing {filename}[/blue]")
        try:
            pdf_reader = PdfReader(file_path)
            text_chunks = []
            
            # Extract and clean text from each page
            for page_num, page in enumerate(tqdm(pdf_reader.pages, desc=f"Reading {filename}", leave=False), 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        cleaned_text = clean_text(page_text)
                        if cleaned_text:
                            text_chunks.append(cleaned_text)
                except Exception as e:
                    console.print(f"[yellow]Warning: Error extracting text from page {page_num} in {filename}: {str(e)}[/yellow]")
                    continue
            
            if not text_chunks:
                console.print(f"[yellow]Warning: No text content extracted from {filename}[/yellow]")
                continue
            
            # Create document entry
            document = {
                "text": "\n\n".join(text_chunks),
                "metadata": {
                    "source": filename,
                    "file_path": file_path,
                    "total_pages": len(pdf_reader.pages)
                }
            }
            
            # Update cache
            cache[file_path] = {
                "hash": file_hash,
                "data": document
            }
            
            documents.append(document)
            console.print(f"[green]Successfully processed {filename}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error processing {filename}: {str(e)}[/red]")
            continue
    
    # Save updated cache
    save_docs_cache(cache)
    return documents

if __name__ == "__main__":
    try:
        console.print("[bold blue]Starting PDF preprocessing...[/bold blue]")
        data_directory = "data"
        documents = read_pdfs_from_directory(data_directory)
        console.print(f"[bold green]✅ Successfully processed {len(documents)} document chunks from {data_directory}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Error: {str(e)}[/bold red]")
        logging.error(f"Main execution error: {str(e)}")
        exit(1)
