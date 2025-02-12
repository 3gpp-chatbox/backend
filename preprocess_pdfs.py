import os
import logging
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
    """Read and preprocess PDFs from a directory."""
    documents = []
    
    if not os.path.exists(directory):
        error_msg = f"Directory {directory} not found"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    if not pdf_files:
        logging.warning(f"No PDF files found in {directory}")
        return documents
    
    console.print(f"[bold green]Found {len(pdf_files)} PDF files to process[/bold green]")
    
    # Process each PDF with progress bar
    for filename in tqdm(pdf_files, desc="Processing PDFs"):
        file_path = os.path.join(directory, filename)
        logging.info(f"Processing {filename}")
        
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
                    logging.warning(f"Error extracting text from page {page_num} in {filename}: {str(e)}")
                    continue
            
            if not text_chunks:
                logging.warning(f"No text content extracted from {filename}")
                continue
            
            # Combine all text and split into meaningful chunks
            full_text = '\n\n'.join(text_chunks)
            document_chunks = chunk_text(full_text)
            
            # Create document entries for each chunk
            for chunk_num, chunk in enumerate(document_chunks, 1):
                if len(chunk.strip()) > 50:  # Only keep chunks with substantial content
                    documents.append({
                        "text": chunk,
                        "metadata": {
                            "source": filename,
                            "file_path": file_path,
                            "chunk_number": chunk_num,
                            "total_chunks": len(document_chunks)
                        }
                    })
            
            logging.info(f"Successfully processed {filename}: created {len(document_chunks)} chunks")
            
        except Exception as e:
            logging.error(f"Error processing {filename}: {str(e)}")
            continue
    
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
