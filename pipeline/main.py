from preprocessor import process_docx
from chunker import create_chunks, DocumentChunker
from embedding_handler import DBHandler
from extractor import ProcedureExtractor
import time
import os
import sys
import json
from typing import List, Dict

# Add parent directory to path for config import
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from config import Gemini_API_KEY


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
    persist_directory = os.path.join(root_folder, "DB", "chroma_db")
    output_directory = os.path.join(root_folder, "graphs", "method_2")

    try:
        # Initialize database handler with ChromaDB
        db_handler = DBHandler(persist_directory=persist_directory)
        doc_id = os.path.basename(final_md_path)
        
        # Process document if needed
        if not os.path.exists(final_md_path):
            print("\n[1/3] Processing DOCX file...")
            return_code = process_docx(docx_path, final_md_path)
            if return_code != 0:
                print("✗ Processing failed. Stopping process.")
                return
        else:
            print(f"\nUsing existing markdown file: {final_md_path}")
            if not db_handler.get_chunks(doc_id):
                print("Creating new chunks...")
                with open(final_md_path, 'r', encoding='utf-8') as f:
                    markdown_text = f.read()
                chunker = DocumentChunker()
                chunks = chunker.process_document(markdown_text)
                stored_count = db_handler.store_chunks(chunks, doc_id)
                print(f"Created and stored {stored_count} new chunks")
            else:
                print("→ Using existing chunks from vector database")

        # Get collection and verify it exists
        try:
            collection = db_handler._create_or_get_collection(doc_id)
            if collection.count() == 0:
                print("✗ No documents found in collection. Stopping.")
                return
            print(f"✓ Using collection with {collection.count()} documents")
        except Exception as e:
            print(f"✗ Failed to get collection: {e}")
            return

        # Extract procedures using Gemini API
        if Gemini_API_KEY:
            procedure_extractor = ProcedureExtractor(api_key=Gemini_API_KEY)
            
            # query for both search and extraction
            query = """
            Search for and extract all relevant details on **Registration Procedures** for **5G Mobility Management**, focusing on the **Initial Registration** and **Periodic Registration Update** procedures.

            ### Retrieval Details:
            Look for passages that describe:
            - **States**: The different User Equipment (UE) and network (AMF) states before, during, and after the registration process.
            - **Transitions**: Descriptions of how the UE moves between states, triggered by events, conditions, and other factors. Include transitions involving different triggers and states.
            - **Events**: Specific triggers that initiate or modify the registration process (e.g., power-on, periodic updates, intersystem changes).
            - **Initial State**: The starting point or initial state in the registration procedure.
            - **Final States**: The outcome states after a successful or failed registration process.
            - **Actions**: Any operations performed by UE/AMF during registration (e.g., message exchanges, authentication).
            - **Timers**: Timers influencing the procedure, especially those related to timeouts or retries.
            - **Error Handling & Failure States**: Details on how registration failures (e.g., congestion, rejection) are handled and the resulting failure states.
            - **NAS Messages**: The key NAS messages exchanged during registration (e.g., REGISTRATION REQUEST, REGISTRATION ACCEPT, REGISTRATION REJECT).
            - **Loops & Iterations**: Information on retry mechanisms, periodic updates, and any iterations that occur during the registration process.

            ### Semantic Similarity:
            Ensure that the retrieval captures **semantically similar** passages, even if the exact terminology is different. For instance, "initial registration" might be referred to as "first-time registration" or "registration initiation." The extraction should handle such variations.  

            """
            
            os.makedirs(output_directory, exist_ok=True)
            print(f"\nProcessing procedures...")
            
            # Use hybrid search with adjusted parameters
            relevant_chunks = db_handler.hybrid_search(
                doc_id=doc_id,
                query=query,
                n_results=20,  # Increased number of results
                min_similarity=0.3  # Lowered similarity threshold
            )
            
            if not relevant_chunks:
                print("✗ No relevant chunks found")
                return

            print(f"→ Found {len(relevant_chunks)} relevant chunks")
            print("\nTop 3 chunks with scores:")
            for i, chunk in enumerate(relevant_chunks[:3], 1):
                print(f"\n{i}. Title: {chunk['title']}")
                print(f"   Content Preview: {chunk['content'][:150]}...")
                print(f"   Semantic Score: {chunk['semantic_score']:.3f}")
                print(f"   Keyword Score: {chunk['keyword_score']:.3f}")
                print(f"   Combined Score: {chunk['combined_score']:.3f}")
            
            # Use the same query for procedure extraction
            procedures = procedure_extractor.extract_procedures_from_query(
                query, relevant_chunks, doc_id
            )
            
            if procedures:
                save_procedure_by_type(procedures, output_directory, Gemini_API_KEY)
            else:
                print("✗ No procedures found")
        else:
            print("\n✗ Gemini API key not found in config.py")

        total_duration = time.time() - total_start_time
        print(f"\n✓ All processing completed in {total_duration:.2f} seconds")
    
    except Exception as e:
        print(f"\n✗ Process failed: {e}")
    finally:
        print("\n=== Processing Finished ===\n")

if __name__ == "__main__":
    main()