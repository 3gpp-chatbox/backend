import json
import os
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from rich import print as rprint
import argparse

console = Console()

def load_cache():
    """Load the preprocessed data from cache"""
    if not os.path.exists("raw_docs_cache.json"):
        console.print("[red]Error: raw_docs_cache.json not found. Please run preprocess_pdfs.py first.[/red]")
        return None
    
    with open("raw_docs_cache.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def show_summary(cache_data):
    """Display summary statistics of the preprocessed data"""
    table = Table(title="Preprocessed Data Summary")
    table.add_column("File Name", style="cyan")
    table.add_column("Total Chunks", style="magenta")
    table.add_column("Avg. Chunk Size", style="green")
    table.add_column("Total Pages", style="yellow")

    for file_path, file_data in cache_data.items():
        file_name = os.path.basename(file_path)
        chunks = file_data['data']
        total_chunks = len(chunks)
        avg_chunk_size = sum(len(chunk['text']) for chunk in chunks) // total_chunks if total_chunks > 0 else 0
        total_pages = chunks[0]['metadata']['total_pages'] if chunks else 0
        
        table.add_row(
            file_name,
            str(total_chunks),
            f"{avg_chunk_size} chars",
            str(total_pages)
        )
    
    console.print(table)

def view_chunks(cache_data, file_pattern=None, chunk_index=None):
    """Display chunks from specified file(s)"""
    for file_path, file_data in cache_data.items():
        file_name = os.path.basename(file_path)
        
        # Skip if doesn't match pattern
        if file_pattern and file_pattern.lower() not in file_name.lower():
            continue
            
        chunks = file_data['data']
        console.print(f"\n[bold cyan]File: {file_name}[/bold cyan]")
        
        for idx, chunk in enumerate(chunks):
            # Skip if not the requested chunk index
            if chunk_index is not None and idx != chunk_index:
                continue
                
            console.print(f"\n[bold green]Chunk {idx + 1}/{len(chunks)}[/bold green]")
            console.print("[bold yellow]Metadata:[/bold yellow]")
            rprint(chunk['metadata'])
            console.print("\n[bold yellow]Content:[/bold yellow]")
            
            # Format the text content with syntax highlighting
            syntax = Syntax(
                chunk['text'],
                "markdown",
                theme="monokai",
                word_wrap=True,
                line_numbers=True,
            )
            console.print(syntax)
            
            if chunk_index is None:
                # Ask to continue after each chunk unless specific chunk was requested
                if not console.input("\nPress Enter to continue (or 'q' to quit): ").lower().startswith('q'):
                    continue
                else:
                    break

def main():
    parser = argparse.ArgumentParser(description="View preprocessed 3GPP document data")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    parser.add_argument("--file", help="Filter by file name (case insensitive)")
    parser.add_argument("--chunk", type=int, help="View specific chunk index")
    args = parser.parse_args()

    cache_data = load_cache()
    if not cache_data:
        return

    if args.summary:
        show_summary(cache_data)
    else:
        view_chunks(cache_data, args.file, args.chunk)

if __name__ == "__main__":
    main() 