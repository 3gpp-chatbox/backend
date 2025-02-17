import os
import logging
import json
import hashlib
from typing import List, Dict
import re
from rich.console import Console
from rich.logging import RichHandler
from tqdm import tqdm
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pdfplumber
from sentence_transformers import SentenceTransformer
import numpy as np
import torch
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Set up rich console logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)

# Initialize NLTK and download required resources
def download_nltk_resources():
    """Download required NLTK resources"""
    resources = [
        ('punkt', 'tokenizers/punkt'),
        ('punkt_tab', 'tokenizers/punkt_tab'),  # Add punkt_tab specifically
        'stopwords',
        'averaged_perceptron_tagger',
        'wordnet',
        'omw-1.4'
    ]
    
    for resource in resources:
        try:
            # Handle resources that need specific paths
            if isinstance(resource, tuple):
                resource_name, resource_path = resource
                try:
                    nltk.data.find(resource_path)
                except LookupError:
                    console.print(f"[yellow]Downloading NLTK resource: {resource_name}[/yellow]")
                    nltk.download(resource_name, quiet=True)
            else:
                console.print(f"[yellow]Checking NLTK resource: {resource}[/yellow]")
                nltk.data.find(resource)
                console.print(f"[green]Found existing resource: {resource}[/green]")
        except LookupError:
            try:
                console.print(f"[yellow]Downloading NLTK resource: {resource}[/yellow]")
                nltk.download(resource, quiet=True)
                console.print(f"[green]Successfully downloaded: {resource}[/green]")
            except Exception as e:
                console.print(f"[red]Failed to download {resource}: {str(e)}[/red]")

# Download NLTK resources
try:
    # Create NLTK data directory if it doesn't exist
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Set NLTK data path
    nltk.data.path.append(nltk_data_dir)
    
    # Download resources
    download_nltk_resources()
except Exception as e:
    console.print(f"[red]Error downloading NLTK resources: {str(e)}[/red]")
    console.print("[yellow]Continuing with limited functionality...[/yellow]")

# Initialize sentence transformer for semantic chunking
model_name = 'all-MiniLM-L6-v2'  # Lightweight but effective model
try:
    # Initialize with silent batch processing
    sentence_transformer = SentenceTransformer(model_name)
    sentence_transformer.encode(['test'], show_progress_bar=False)  # Warm up and test
    console.print(f"[green]Successfully loaded sentence transformer model: {model_name}[/green]")
except Exception as e:
    console.print(f"[red]Error loading sentence transformer: {str(e)}[/red]")
    sentence_transformer = None

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

def is_title_page_content(text: str) -> bool:
    """Identify if text is likely from a title page."""
    title_page_patterns = [
        r'Technical\s+Specification',
        r'Technical\s+Report',
        r'3rd Generation Partnership Project',
        r'3GPP Organizational Partners',
        r'ARIB, ATIS, CCSA, ETSI, TSDSI, TTA, TTC',
        r'Copyright Notification',
        r'No part may be reproduced',
        r'All rights reserved',
        r'Legal Notice'
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in title_page_patterns)

def is_toc_content(text: str) -> bool:
    """Identify if text is likely from table of contents."""
    toc_patterns = [
        r'^Contents$',
        r'^Table of Contents$',
        r'^\d+\.+\s*[A-Z].*\.+\s*\d+$',  # Matches "1. Introduction..............10"
        r'^\s*Foreword\s*$',
        r'^\s*Introduction\s*$',
        r'^\s*Scope\s*$',
        r'^\s*References\s*$'
    ]
    
    # Count lines that look like TOC entries
    lines = text.split('\n')
    toc_like_lines = sum(1 for line in lines if re.search(r'\.{3,}|…+\s*\d+$', line))
    
    return (
        any(re.search(pattern, text, re.MULTILINE) for pattern in toc_patterns) or
        (toc_like_lines / len(lines) if lines else 0) > 0.3  # If >30% of lines look like TOC entries
    )

def is_index_or_appendix_content(text: str) -> bool:
    """Identify if text is likely from an index or appendix cover page."""
    patterns = [
        r'^Annex\s+[A-Z]\s*$',
        r'^Index$',
        r'^List of figures$',
        r'^List of tables$',
        r'^Bibliography$',
        r'^History$'
    ]
    return any(re.search(pattern, text, re.MULTILINE) for pattern in patterns)

def extract_text_from_pdf(file_path: str) -> List[str]:
    """Extract text from PDF using pdfplumber with OCR fallback"""
    text_pages = []
    
    # Try pdfplumber first
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and len(text.strip()) > 0:
                    text_pages.append(text)
                else:
                    # If page has no text, try OCR
                    images = convert_from_path(file_path, first_page=page.page_number+1, last_page=page.page_number+1)
                    for image in images:
                        text = pytesseract.image_to_string(image)
                        if text.strip():
                            text_pages.append(text)
    except Exception as e:
        console.print(f"[red]Error extracting text: {str(e)}[/red]")
        return []
    
    return text_pages

def semantic_chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into semantically meaningful chunks optimized for 3GPP documents"""
    try:
        # First, try to split into sentences using punkt
        sentences = sent_tokenize(text)
    except LookupError:
        # Fallback to simple splitting if NLTK resources aren't available
        console.print("[yellow]Warning: NLTK sentence tokenizer not available, using simple splitting[/yellow]")
        sentences = []
        for paragraph in text.split('\n'):
            for possible_sentence in re.split(r'(?<=[.!?])\s+', paragraph):
                if possible_sentence.strip():
                    sentences.append(possible_sentence.strip())
    
    # Create chunks using LangChain's RecursiveCharacterTextSplitter with 3GPP-specific separators
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=200,  # Overlap to maintain context
        length_function=len,
        separators=[
            "\n\n",  # Paragraph breaks
            "\n",    # Line breaks
            ".",     # Sentence endings
            ";",     # Common in 3GPP for lists
            ":",     # Common in 3GPP for definitions
            " ",     # Word boundaries
            ""       # Character level
        ]
    )
    
    # Group sentences into initial chunks
    chunks = text_splitter.split_text(text)
    
    # Further process chunks to ensure semantic coherence
    processed_chunks = []
    current_section = None
    current_chunk = []
    
    for chunk in chunks:
        # Clean the chunk
        chunk = clean_text(chunk)
        if not chunk:
            continue
        
        # Check for section headings
        lines = chunk.split('\n')
        for line in lines:
            if is_section_heading(line):
                # Save previous chunk if it exists
                if current_chunk:
                    processed_text = '\n'.join(current_chunk)
                    if len(processed_text) > 100:  # Minimum chunk size
                        if current_section:
                            processed_text = f"{current_section}\n{processed_text}"
                        processed_chunks.append(processed_text)
                current_section = line
                current_chunk = []
            else:
                current_chunk.append(line)
        
        # Get sentence embeddings if transformer is available
        if sentence_transformer and current_chunk:
            try:
                chunk_text = '\n'.join(current_chunk)
                chunk_sentences = sent_tokenize(chunk_text)
                
                if chunk_sentences:
                    # Calculate embeddings silently
                    embeddings = sentence_transformer.encode(
                        chunk_sentences,
                        show_progress_bar=False,
                        batch_size=32
                    )
                    
                    # Calculate sentence similarities
                    similarities = np.dot(embeddings, embeddings.T)
                    
                    # Only keep sentences that are semantically related
                    coherent_sentences = []
                    prev_embedding = None
                    
                    for i, sentence in enumerate(chunk_sentences):
                        if prev_embedding is None or np.dot(embeddings[i], prev_embedding) > 0.5:
                            coherent_sentences.append(sentence)
                            prev_embedding = embeddings[i]
                    
                    if coherent_sentences:
                        processed_text = ' '.join(coherent_sentences)
                        if len(processed_text) > 100:  # Minimum chunk size
                            if current_section:
                                processed_text = f"{current_section}\n{processed_text}"
                            processed_chunks.append(processed_text)
            except Exception as e:
                console.print(f"[yellow]Warning: Error in semantic processing: {str(e)}[/yellow]")
                # Continue with the original chunk if semantic processing fails
                if current_chunk:
                    processed_text = '\n'.join(current_chunk)
                    if len(processed_text) > 100:
                        if current_section:
                            processed_text = f"{current_section}\n{processed_text}"
                        processed_chunks.append(processed_text)
    
    # Add the last chunk if it exists
    if current_chunk:
        processed_text = '\n'.join(current_chunk)
        if len(processed_text) > 100:
            if current_section:
                processed_text = f"{current_section}\n{processed_text}"
            processed_chunks.append(processed_text)
    
    return processed_chunks

def extract_attach_procedure_elements(text: str) -> Dict[str, List[str]]:
    """Extract specific elements related to the attach procedure"""
    elements = {
        'states': [],
        'actions': [],
        'events': [],
        'parameters': [],
        'flow_steps': [],
        'conditionals': [],
        'metadata': []
    }
    
    # State patterns for attach procedure
    state_patterns = [
        r'(?:UE|MS)\s+(?:in|enters?|transitions?\s+to)\s+EMM-(?:DEREGISTERED|REGISTERED)(?:\.[\w-]+)?',
        r'(?:UE|MS)\s+(?:is|becomes?)\s+(?:attached|detached)',
        r'EMM-(?:REGISTERED|DEREGISTERED)\.(?:NORMAL-SERVICE|ATTEMPTING-TO-ATTACH|LIMITED-SERVICE)',
        r'(?:MME|eNB)\s+(?:in|enters?)\s+(?:CONNECTED|IDLE)\s+state',
        r'(?:AUTHENTICATION|SECURITY MODE|ATTACH)\s+(?:INITIATED|IN_PROGRESS|COMPLETED)',
        r'(?:UE|MS)\s+(?:powers?\s+on|starts?\s+up|boots?\s+up)',
        r'(?:UE|MS)\s+(?:not\s+attached|no\s+network\s+connection)',
        r'(?:UE|MS)\s+(?:can\s+access|has\s+access\s+to)\s+(?:services|network)',
        r'(?:UE|MS)\s+(?:gains?|obtains?)\s+(?:service|network)\s+access',
        r'(?:UE|MS)\s+(?:ready\s+for|available\s+for)\s+service'
    ]
    
    # Action patterns for attach procedure
    action_patterns = [
        r'(?:UE|MS)\s+(?:sends?|initiates?|transmits?)\s+ATTACH\s+REQUEST',
        r'MME\s+(?:initiates?|starts?)\s+authentication(?:\s+procedure)?',
        r'MME\s+(?:sends?|transmits?)\s+SECURITY\s+MODE\s+COMMAND',
        r'MME\s+(?:sends?|transmits?)\s+ATTACH\s+ACCEPT',
        r'(?:UE|MS)\s+(?:sends?|responds?\s+with)\s+ATTACH\s+COMPLETE',
        r'(?:generate|verify)\s+(?:AUTH|AUTN|RAND|RES|XRES)',
        r'(?:derive|compute)\s+(?:K_ASME|NAS\s+keys)'
    ]
    
    # Event patterns for attach procedure
    event_patterns = [
        r'(?:upon|when|after)\s+receiving\s+ATTACH\s+REQUEST',
        r'(?:on|upon)\s+successful\s+authentication',
        r'(?:after|when)\s+security\s+mode\s+(?:complete|success)',
        r'T3410\s+(?:starts?|expires?|stops?)',  # Attach attempt timer
        r'T3411\s+(?:starts?|expires?|stops?)',  # Attach retry timer
        r'T3450\s+(?:starts?|expires?|stops?)'   # Attach accept timer
    ]
    
    # Parameter patterns for attach procedure
    parameter_patterns = [
        r'(?:IMSI|GUTI|TMSI|OLD\s+GUTI)',
        r'(?:TAI|LAI|RAI|PLMN)',
        r'(?:KSI|eKSI|KASME)',
        r'(?:AUTH|AUTN|RAND|RES|XRES)',
        r'(?:NAS-MAC|NAS\s+COUNT)',
        r'UE\s+(?:network|security)\s+capabilities',
        r'(?:EPS|DEFAULT)\s+bearer\s+context',
        r'ESM\s+message\s+container'
    ]
    
    # Flow step patterns for attach procedure
    flow_patterns = [
        r'Step\s+\d+[:.]\s*(?:The\s+)?(?:UE|MME)\s+(?:sends?|performs?)',
        r'(?:First|Then|Next|Finally)\s+(?:the\s+)?(?:UE|MME)\s+(?:shall|must|may)',
        r'(?:After|Before|Following)\s+(?:the|this)\s+(?:step|procedure|message)',
        r'(?:If|When|In\s+case)\s+(?:the|this)\s+(?:condition|check|verification)\s+(?:succeeds|fails)'
    ]
    
    # Conditional patterns for attach procedure
    conditional_patterns = [
        r'if\s+authentication\s+(?:successful|failed)',
        r'when\s+security\s+mode\s+(?:completed|rejected)',
        r'if\s+(?:IMSI|GUTI|TMSI)\s+is\s+(?:valid|invalid|available)',
        r'if\s+UE\s+(?:is|was)\s+in\s+EMM-(?:REGISTERED|DEREGISTERED)',
        r'when\s+default\s+bearer\s+is\s+(?:established|activated)',
        r'if\s+T34[0-9]+\s+(?:expires|running)'
    ]
    
    # Metadata patterns for attach procedure
    metadata_patterns = [
        r'Message\s+Type:\s*(?:0x[0-9A-F]{2}|[0-9]+)',
        r'Protocol\s+(?:Discriminator|Identifier):\s*(?:0x[0-9A-F]{2}|[0-9]+)',
        r'T34[0-9]+\s*=\s*\d+\s*(?:sec|seconds)',
        r'Message\s+ID:\s*(?:0x[0-9A-F]{4}|[0-9]+)',
        r'EMM\s+cause:\s*(?:0x[0-9A-F]{2}|[0-9]+)',
        r'(?:NAS|EPS)\s+security\s+context:\s*\d+'
    ]
    
    # Extract elements using patterns
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Extract states
        for pattern in state_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['states'].append(line)
                
        # Extract actions
        for pattern in action_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['actions'].append(line)
                
        # Extract events
        for pattern in event_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['events'].append(line)
                
        # Extract parameters
        for pattern in parameter_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['parameters'].append(line)
                
        # Extract flow steps
        for pattern in flow_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['flow_steps'].append(line)
                
        # Extract conditionals
        for pattern in conditional_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['conditionals'].append(line)
                
        # Extract metadata
        for pattern in metadata_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                elements['metadata'].append(line)
    
    return elements

def clean_text(text: str) -> str:
    """Enhanced text cleaning specifically for 3GPP attach procedure"""
    try:
        if not isinstance(text, str):
            text = str(text, errors='ignore')
        
        # Skip title pages and TOC
        if is_title_page_content(text) or is_toc_content(text):
            return ""
        
        # Extract attach procedure elements
        elements = extract_attach_procedure_elements(text)
        
        # 3GPP-specific cleanups
        text = re.sub(r'3GPP\s+TS\s+\d+\.\d+\.\d+\s+V\d+\.\d+\.\d+', '', text)  # Remove spec numbers
        text = re.sub(r'Release\s+\d+', '', text)  # Remove release numbers
        text = re.sub(r'(?<=\d)[\-\s](?=G)', '', text)  # Fix "5-G" to "5G"
        text = re.sub(r'(?<=\d)[\-\s](?=GPP)', '', text)  # Fix "3-GPP" to "3GPP"
        
        # Fix common 3GPP terms
        text = re.sub(r'e\s*-?\s*UTRAN', 'E-UTRAN', text, flags=re.IGNORECASE)
        text = re.sub(r'e\s*-?\s*NodeB', 'eNodeB', text, flags=re.IGNORECASE)
        text = re.sub(r'g\s*-?\s*NodeB', 'gNodeB', text, flags=re.IGNORECASE)
        text = re.sub(r'(?i)ue\s+equipment', 'UE', text)
        
        # Fix attach procedure specific terms
        text = re.sub(r'(?i)attach\s+request', 'ATTACH REQUEST', text)
        text = re.sub(r'(?i)attach\s+accept', 'ATTACH ACCEPT', text)
        text = re.sub(r'(?i)attach\s+complete', 'ATTACH COMPLETE', text)
        text = re.sub(r'(?i)attach\s+reject', 'ATTACH REJECT', text)
        text = re.sub(r'(?i)security\s+mode\s+command', 'SECURITY MODE COMMAND', text)
        text = re.sub(r'(?i)authentication\s+request', 'AUTHENTICATION REQUEST', text)
        
        try:
            # Try to tokenize into sentences using NLTK
            sentences = sent_tokenize(text)
        except LookupError:
            # Fallback to simple sentence splitting
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        
        cleaned_sentences = []
        
        for sentence in sentences:
            # Skip short sentences and known patterns
            if len(sentence) < 5 or any(pattern in sentence.lower() for pattern in ['page', 'etsi', '3gpp ts']):
                continue
            
            # Remove common PDF artifacts and normalize text
            sentence = re.sub(r'\bPage\s+\d+\s+of\s+\d+\b', '', sentence)
            sentence = re.sub(r'\.{3,}', '...', sentence)
            sentence = re.sub(r'\s+', ' ', sentence)
            
            # Fix section references
            sentence = re.sub(r'clause\s+(\d+\.[\d.]*)', r'Clause \1', sentence, flags=re.IGNORECASE)
            sentence = re.sub(r'section\s+(\d+\.[\d.]*)', r'Section \1', sentence, flags=re.IGNORECASE)
            
            # Remove lines that are just numbers or section numbers
            if not sentence.strip().isdigit() and not re.match(r'^\d+(\.\d+)*$', sentence.strip()):
                cleaned_sentences.append(sentence.strip())
        
        # Join sentences back together
        text = ' '.join(cleaned_sentences)
        
        # Remove very short paragraphs and normalize spacing
        paragraphs = [p.strip() for p in text.split('\n\n')]
        paragraphs = [p for p in paragraphs if len(p) > 50]  # Minimum paragraph size
        
        return '\n\n'.join(paragraphs)
        
    except Exception as e:
        logging.warning(f"Error in clean_text: {str(e)}")
        return ""

def is_section_heading(line: str) -> bool:
    """Check if a line is a section heading in 3GPP documents."""
    # 3GPP-specific section heading patterns
    heading_patterns = [
        r'^\d+(?:\.\d+)*\s+[A-Z]',  # Numbered sections (e.g., "4.1 Overview")
        r'^Annex [A-Z](?:\s+\([Nn]ormative|[Ii]nformative\))?',  # Annexes with optional type
        r'^Table \d+(?:\.\d+)*(?:-\d+)*',  # Tables with possible subsections or ranges
        r'^Figure \d+(?:\.\d+)*(?:-\d+)*',  # Figures with possible subsections or ranges
        r'^[A-Z][A-Za-z\s]+$',  # All caps or Title Case headings
        r'^Scope$',  # Common 3GPP sections
        r'^References$',
        r'^Definitions(?:,\s+symbols\s+and\s+abbreviations)?$',
        r'^Abbreviations$',
        r'^General$',
        r'^Introduction$',
        r'^Procedures?$',
        r'^Requirements?$'
    ]
    
    line = line.strip()
    
    # Skip lines that are too long to be headings
    if len(line) > 100:
        return False
        
    # Skip lines that are likely page headers or footers
    if re.search(r'3GPP\s+TS|Page|Release', line):
        return False
        
    return any(re.match(pattern, line) for pattern in heading_patterns)

def chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
    """Split text into meaningful chunks optimized for attach procedure flow"""
    chunks = []
    current_chunk = []
    current_heading = None
    current_size = 0
    
    # Extract attach procedure elements first
    elements = extract_attach_procedure_elements(text)
    
    # Split into lines while preserving paragraph structure
    lines = text.split('\n')
    in_attach_procedure = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect start of attach procedure section
        if re.search(r'(?i)attach\s+procedure|EPS\s+attach|initial\s+attach', line):
            in_attach_procedure = True
            if current_chunk and current_size > 50:
                chunk_text = '\n'.join(current_chunk)
                if current_heading:
                    chunk_text = f"{current_heading}\n{chunk_text}"
                chunks.append(chunk_text)
            current_chunk = [line]
            current_heading = line
            current_size = len(line)
            continue
        
        # Detect end of attach procedure section
        if in_attach_procedure and re.search(r'(?i)end\s+of\s+attach|completion\s+of\s+attach', line):
            in_attach_procedure = False
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                if current_heading:
                    chunk_text = f"{current_heading}\n{chunk_text}"
                chunks.append(chunk_text)
            current_chunk = []
            current_heading = None
            current_size = 0
            continue
        
        # Skip unnecessary sections
        if is_index_or_appendix_content(line):
            if current_chunk and current_size > 50:
                chunk_text = '\n'.join(current_chunk)
                if current_heading:
                    chunk_text = f"{current_heading}\n{chunk_text}"
                chunks.append(chunk_text)
            current_chunk = []
            current_size = 0
            continue
        
        if is_section_heading(line):
            # Save previous chunk if it exists
            if current_chunk and current_size > 50:
                chunk_text = '\n'.join(current_chunk)
                if current_heading:
                    chunk_text = f"{current_heading}\n{chunk_text}"
                chunks.append(chunk_text)
            
            current_heading = line
            current_chunk = []
            current_size = 0
        else:
            # Skip lines that are just numbers or very short
            if len(line) <= 5 or line.isdigit():
                continue
            
            # Check if line contains any attach procedure elements
            is_attach_element = False
            for element_type, element_list in elements.items():
                if any(element in line for element in element_list):
                    is_attach_element = True
                    break
            
            if is_attach_element or in_attach_procedure:
                current_chunk.append(line)
                current_size += len(line)
                
                # Split if chunk is too large, but try to break at procedure boundaries
                if current_size > max_chunk_size:
                    # Try to find a good breaking point
                    break_point = -1
                    for i, l in enumerate(current_chunk):
                        if re.search(r'(?i)step\s+\d+|then|next|finally', l):
                            break_point = i
                    
                    if break_point != -1:
                        # Split at the procedure step
                        first_part = current_chunk[:break_point]
                        if first_part:
                            chunk_text = '\n'.join(first_part)
                            if current_heading:
                                chunk_text = f"{current_heading}\n{chunk_text}"
                            chunks.append(chunk_text)
                        current_chunk = current_chunk[break_point:]
                        current_size = sum(len(l) for l in current_chunk)
                    else:
                        # No good breaking point found, split as is
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
    
    # Filter out chunks that are too short or look like TOC/index
    chunks = [chunk for chunk in chunks 
             if len(chunk) > 100  # Minimum chunk size
             and not is_toc_content(chunk)
             and not is_title_page_content(chunk)]
    
    # Sort chunks to ensure attach procedure flow is preserved
    def get_chunk_order(chunk):
        if re.search(r'(?i)initial\s+attach|attach\s+procedure', chunk):
            return 0
        if re.search(r'(?i)attach\s+request', chunk):
            return 1
        if re.search(r'(?i)authentication', chunk):
            return 2
        if re.search(r'(?i)security\s+mode', chunk):
            return 3
        if re.search(r'(?i)attach\s+accept', chunk):
            return 4
        if re.search(r'(?i)attach\s+complete', chunk):
            return 5
        return 6
    
    chunks.sort(key=get_chunk_order)
    
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
            documents.extend(cache[file_path]["data"])
            continue
        
        console.print(f"[blue]Processing {filename}[/blue]")
        try:
            # Extract text using enhanced PDF extraction
            full_text = extract_text_from_pdf(file_path)
            
            if not full_text:
                console.print(f"[yellow]Warning: No text content extracted from {filename}[/yellow]")
                continue
            
            # Join all text and create semantic chunks
            combined_text = "\n\n".join(full_text)
            text_chunks = semantic_chunk_text(combined_text)
            
            # Create document entries for each chunk
            file_documents = []
            for chunk_idx, chunk in enumerate(text_chunks):
                document = {
                    "text": chunk,
                    "metadata": {
                        "source": filename,
                        "file_path": file_path,
                        "chunk_index": chunk_idx,
                        "total_chunks": len(text_chunks),
                        "total_pages": len(full_text)
                    }
                }
                file_documents.append(document)
            
            # Update cache with chunked documents
            cache[file_path] = {
                "hash": file_hash,
                "data": file_documents
            }
            
            documents.extend(file_documents)
            console.print(f"[green]Successfully processed {filename} into {len(file_documents)} chunks[/green]")
            
        except Exception as e:
            console.print(f"[red]Error processing {filename}: {str(e)}[/red]")
            continue
    
    # Save updated cache
    save_docs_cache(cache)
    return documents

if __name__ == "__main__":
    try:
        console.print("[bold blue]Starting PDF preprocessing...[/bold blue]")
        data_directory = os.path.join("backend", "data")
        documents = read_pdfs_from_directory(data_directory)
        console.print(f"[bold green]✅ Successfully processed {len(documents)} document chunks from {data_directory}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Error: {str(e)}[/bold red]")
        logging.error(f"Main execution error: {str(e)}")
        exit(1)
