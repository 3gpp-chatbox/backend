from preprocessor import process_docx
from chunker import create_chunks, DocumentChunker
from embedding_handler import DBHandler
from extractor import ProcedureExtractor
import time
import os
import sys
import json
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
Gemini_API_KEY = os.getenv('GEMINI_API_KEY')

def save_procedure_by_type(procedures: List[Dict], output_directory: str, api_key: str):
    """Dynamically save procedures based on their types"""
    
    # Group procedures by type
    procedure_groups = {}
    for proc in procedures:
        # Get procedure type from procedure name 
        proc_type = proc.get('procedure_name', '').lower().replace(' ', '_')
        if not proc_type:  # Skip if no procedure name found
            print(f"Warning: Procedure found without name: {proc}")
            continue
            
        if proc_type not in procedure_groups:
            procedure_groups[proc_type] = []
        procedure_groups[proc_type].append(proc)
    
    # Create directories if they don't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Save each procedure group
    for proc_type, procs in procedure_groups.items():
        # Save procedures
        output_path = os.path.join(output_directory, f"{proc_type}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(procs, f, indent=2, ensure_ascii=False)
        print(f"→ Saved {proc_type} procedures to {output_path}")
        
        # Generate and save graph
        # graphs = extract_nodes_and_edges(procs, api_key)
        # if graphs:
        #     graph_path = os.path.join(graph_directory, f"{safe_name}_graph.json")
        #     with open(graph_path, 'w', encoding='utf-8') as f:
        #         json.dump(graphs, f, indent=2, ensure_ascii=False)
        #     print(f"→ Saved {proc_type} graph to {graph_path}")

def main():
    total_start_time = time.time()
    print("\n=== Starting Document Processing ===")
    
    # Setup paths
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docx_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.docx")
    final_md_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.md")

    try:
        # Process document if needed
        if not os.path.exists(final_md_path):
            print("\n[1/2] Processing DOCX file...")
            return_code = process_docx(docx_path, final_md_path)
            if return_code != 0:
                print("✗ Processing failed. Stopping process.")
                return
        else:
            print(f"\nUsing existing markdown file: {final_md_path}")
        
        # Create chunks
        print("\n[2/2] Creating chunks...")
        chunks = create_chunks(final_md_path)
        
        if not chunks:
            print("✗ No chunks created")
            return

        total_duration = time.time() - total_start_time
        print(f"\n✓ All processing completed in {total_duration:.2f} seconds")
    
    except Exception as e:
        print(f"\n✗ Process failed: {e}")
    finally:
        print("\n=== Processing Finished ===\n")

if __name__ == "__main__":
    main()