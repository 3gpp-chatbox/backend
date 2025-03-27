# using preprocessing output go through the following steps to generate chunks:

# 1. Document-Based Chunking as a Foundation
# 2. Semantic Chunking

import re
from typing import List, Dict
import spacy
from spacy.language import Language
from embedding_handler import DBHandler
import os
import json

class DocumentChunker:
    def __init__(self, nlp: Language = None):
        # Load spaCy model for semantic analysis
        self.nlp = nlp or spacy.load("en_core_web_sm")
        self.max_chunk_size = 500  # Maximum characters per chunk
        self.overlap = 25  # Overlap between chunks

    def process_document(self, markdown_text: str) -> List[Dict]:
        """
        Process document through both document-based and semantic chunking.
        """
        # First pass: Document-based chunking
        doc_chunks = self._document_based_chunking(markdown_text)
        
        # Second pass: Semantic chunking
        semantic_chunks = self._semantic_chunking(doc_chunks)
        
        return semantic_chunks

    def _document_based_chunking(self, markdown_text: str) -> List[Dict]:
        """
        First-level chunking based on document structure.
        Splits content into sections based on headers.
        """
        chunks = []
        current_chunk = {"title": "", "content": [], "level": 0}
        
        lines = markdown_text.splitlines()
        
        for line in lines:
            if line.startswith('#'):
                # Save previous chunk if it has content
                if current_chunk["content"]:
                    chunks.append(current_chunk)
                
                # Start new chunk
                level = len(re.match(r'^#+', line).group())
                title = line.lstrip('#').strip()
                current_chunk = {
                    "title": title,
                    "content": [],
                    "level": level
                }
            else:
                if line.strip():
                    current_chunk["content"].append(line)
        
        # Add the last chunk
        if current_chunk["content"]:
            chunks.append(current_chunk)
        
        return chunks

    def _semantic_chunking(self, doc_chunks: List[Dict]) -> List[Dict]:
        """
        Second-level chunking based on semantic coherence.
        Processes each document chunk into semantic units.
        """
        semantic_chunks = []
        
        for doc_chunk in doc_chunks:
            # Join content into a single text
            text = ' '.join(doc_chunk["content"])
            
            # Process with spaCy for sentence boundaries
            doc = self.nlp(text)
            
            current_chunk = {
                "title": doc_chunk["title"],
                "content": "",
                "level": doc_chunk["level"]
            }
            
            # Build chunks respecting sentence boundaries
            for sent in doc.sents:
                if len(current_chunk["content"]) + len(str(sent)) > self.max_chunk_size:
                    if current_chunk["content"]:
                        semantic_chunks.append(current_chunk)
                        current_chunk = {
                            "title": doc_chunk["title"],
                            "content": "",
                            "level": doc_chunk["level"]
                        }
                
                current_chunk["content"] += str(sent) + " "
            
            # Add the last chunk
            if current_chunk["content"]:
                semantic_chunks.append(current_chunk)
        
        return semantic_chunks

def create_chunks(markdown_file: str, db_path: str = None) -> List[Dict]:
    """Main function to create chunks from a markdown file, store in DB and save to files."""
    try:
        # Initialize DB handler with ChromaDB
        db_handler = DBHandler(persist_directory="DB/chroma_db")
        doc_id = os.path.basename(markdown_file)
        
        # Check if chunks already exist in DB
        existing_chunks = db_handler.get_chunks(doc_id)
        if existing_chunks:
            print(f"Found {len(existing_chunks)} existing chunks in DB")
            chunks = existing_chunks
        else:
            # Create new chunks if none exist
            print("Creating new chunks...")
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            
            chunker = DocumentChunker()
            chunks = chunker.process_document(markdown_text)
            
            # Store in DB
            stored_count = db_handler.store_chunks(chunks, doc_id)
            print(f"Created and stored {stored_count} chunks in DB")

        # Save chunks to files (both JSON and MD)
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "processed_data")
        os.makedirs(output_dir, exist_ok=True)
        base_filename = os.path.splitext(os.path.basename(markdown_file))[0]
        
        # Save as JSON
        json_file = os.path.join(output_dir, f"{base_filename}_chunks.json")
        chunks_with_ids = [{"chunk_id": i+1, **chunk} for i, chunk in enumerate(chunks)]
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(chunks_with_ids, f, indent=2, ensure_ascii=False)
        
        # Save as Markdown
        md_file = os.path.join(output_dir, f"{base_filename}_chunks.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            for chunk in chunks_with_ids:
                f.write(f"## Chunk {chunk['chunk_id']}: {chunk['title']}\n\n")
                f.write(f"Level: {chunk['level']}\n\n")
                f.write(f"{chunk['content']}\n\n")
                f.write("---\n\n")
        
        print(f"Saved chunks to:")
        print(f"- JSON: {json_file}")
        print(f"- Markdown: {md_file}")
        
        # Print example chunk
        if chunks:
            print("\nExample chunk:")
            print(json.dumps(chunks_with_ids[0], indent=2))
            
        return chunks
        
    except Exception as e:
        print(f"Error during chunking: {e}")
        return []






