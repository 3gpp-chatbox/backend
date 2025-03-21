import re
from typing import Dict, List
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rich.console import Console

console = Console()

def chunk_text_by_headings(text: str) -> List[Dict[str, str]]:
    """
    Chunks the document into sections based on heading levels, then ensures each section
    is within a reasonable size limit using RecursiveCharacterTextSplitter.
    
    Args:
        text (str): The cleaned text of the document.
        
    Returns:
        List[Dict[str, str]]: A list of dictionaries containing 'heading' and 'content' for each chunk.
    """
    # Regular expression to match headings with numbers (e.g., 5, 5.1, 5.1.1, etc.)
    heading_pattern = r'^\s*(\d+(\.\d+)*)(\s+.*)$'
    
    chunks = []
    current_chunk = None
    
    # Split the document by newlines
    lines = text.split('\n')
    
    # Initialize the splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Maximum characters per chunk
        chunk_overlap=200,  # Number of characters to overlap between chunks
        separators=["\n\n", "\n", " ", ""]  # Try to split on paragraph breaks first
    )
    
    for line in lines:
        # Skip lines that are just repeated dashes (--- or ------ etc)
        if re.match(r'^-+$', line.strip()):
            continue
            
        heading_match = re.match(heading_pattern, line.strip())
        
        if heading_match:
            # If we have a current chunk, process and save it
            if current_chunk:
                # Split the content if it's too large
                content_text = "\n".join(current_chunk['content'])
                if len(content_text) > 2000:  # Only split if content is large
                    split_chunks = text_splitter.split_text(content_text)
                    # Create multiple chunks with same heading but split content
                    for i, split_chunk in enumerate(split_chunks):
                        chunks.append({
                            'heading': f"{current_chunk['heading']} (Part {i+1})",
                            'content': split_chunk.split('\n'),
                            'level': current_chunk['level']
                        })
                else:
                    chunks.append(current_chunk)
            
            # Extract the heading level and heading text
            heading_number = heading_match.group(1).strip()  # e.g., "5", "5.1", etc.
            heading_text = heading_match.group(3).strip()   # The text following the number (e.g., "Overview")
            
            # Determine the heading level based on the number of periods in the heading number
            heading_level = heading_number.count('.') + 1
            
            current_chunk = {'heading': heading_text, 'content': [], 'level': heading_level}
        
        elif current_chunk:
            # Add the line to the current chunk's content
            current_chunk['content'].append(line.strip())
    
    # Don't forget to process the last chunk
    if current_chunk:
        content_text = "\n".join(current_chunk['content'])
        if len(content_text) > 2000:
            split_chunks = text_splitter.split_text(content_text)
            for i, split_chunk in enumerate(split_chunks):
                chunks.append({
                    'heading': f"{current_chunk['heading']} (Part {i+1})",
                    'content': split_chunk.split('\n'),
                    'level': current_chunk['level']
                })
        else:
            chunks.append(current_chunk)
    
    return chunks

def save_chunks_to_markdown(chunks: List[Dict[str, str]], output_file: str):
    """
    Saves the chunks into a markdown file.
    
    Args:
        chunks (List[Dict[str, str]]): The list of chunks to save.
        output_file (str): The file path where the chunks should be saved.
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as file:
        for chunk in chunks:
            # Write the heading with the corresponding number of '#' symbols
            file.write(f"{'#' * chunk['level']} {chunk['heading']}\n")
            
            # Write the content under the heading
            for content_line in chunk['content']:
                file.write(f"{content_line}\n")
            
            file.write("\n" + "-" * 50 + "\n\n")  # Optional separator for clarity

class StructuralChunker:
    def __init__(self):
        self.chunks = []
        
    def chunk_markdown_file(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # First, preserve section numbers by converting them to a format that won't be affected by splitting
            def preserve_section_numbers(match):
                section = match.group(0)
                # Keep the original section number and title
                return f"SECTION_MARKER{section}"
            
            # Preserve section numbers before splitting
            preserved_content = re.sub(r'^(\d+(?:\.\d+)*)\s+([^\n]+)', preserve_section_numbers, content, flags=re.MULTILINE)
            
            # Use RecursiveCharacterTextSplitter as before
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_text(preserved_content)
            
            # Restore section numbers after splitting
            processed_chunks = []
            for chunk in chunks:
                # Restore original section numbers
                restored_chunk = chunk.replace("SECTION_MARKER", "")
                processed_chunks.append(restored_chunk)
            
            self.chunks = processed_chunks
            console.print(f"[green]Created {len(processed_chunks)} chunks[/green]")
            return processed_chunks
            
        except Exception as e:
            console.print(f"[red]Error during structural chunking: {str(e)}[/red]")
            raise
            
    def save_chunks(self, chunks: List[str], output_file: str):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for i, chunk in enumerate(chunks, 1):
                    f.write(f"\n{'='*80}\nChunk {i}:\n{'='*80}\n\n")
                    f.write(chunk)
                    f.write("\n\n")
                    
            console.print(f"[green]✓ Saved {len(chunks)} chunks to {output_file}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error saving chunks: {str(e)}[/red]")
            raise

if __name__ == "__main__":
    try:
        base_dir = Path(__file__).parent.parent
        input_file = base_dir / "processed_data" / "cleaned_TS_24.501.md"
        output_file = base_dir / "processed_data" / "chunked_TS_24.501.md"
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found at: {input_file}")
            
        console.print(f"[yellow]Processing file: {input_file}[/yellow]")
        
        chunker = StructuralChunker()
        chunks = chunker.chunk_markdown_file(str(input_file))
        chunker.save_chunks(chunks, str(output_file))
        
    except Exception as e:
        console.print(f"[red]Failed to execute structural chunking: {str(e)}[/red]")
