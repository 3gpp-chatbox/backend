from preprocessor import process_docx
from chunker import create_chunks, DocumentChunker
from embedding_handler import DBHandler
from extractor import ProcedureExtractor
from extractGraphData import extract_nodes_and_edges
import time
import os
import sys
import json

# Add parent directory to path for config import
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from config import Gemini_API_KEY


def main():
    total_start_time = time.time()
    print("\n=== Starting Document Processing ===")
    
    # Setup paths
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docx_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.docx")
    final_md_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.md")
    persist_directory = os.path.join(root_folder, "DB", "chroma_db")
    output_directory = os.path.join(root_folder, "output")
    graph_directory = os.path.join(root_folder, "graphs")

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
            
            # Define a single query for both search and extraction
            query = """
            Find and extract information about Registration Procedures in 5G NAS:

            1. Initial Registration procedure:
            2. Periodic Registration update procedure:

            Extract all relevant details about the procedures from the context provided:
               - Triggers and causes
               - State transitions (5GMM/EMM)
               - Message flows and NAS exchanges
               - Error handling and retries
               - Expected outcomes

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
                # Organize procedures by category
                categorized = {}
                for proc in procedures:
                    category = proc['procedure_category']
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(proc)

                # Save results by category
                for category, procs in categorized.items():
                    output_path = os.path.join(
                        output_directory, 
                        f"{category.lower().replace(' ', '_')}.json"
                    )
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(procs, f, indent=2, ensure_ascii=False)
                    print(f"→ Saved {len(procs)} {category} procedures to {output_path}")

                    # Extract and store graph data for each procedure
                    print(f"\nProcessing graph data for {category}...")
                    procedure_graphs = extract_nodes_and_edges(procs, Gemini_API_KEY)
                    
                    # Save individual graph files
                    for proc_name, graph_data in procedure_graphs.items():
                        if graph_data and graph_data.get("nodes"):
                            # Create graphs directory if it doesn't exist
                            os.makedirs(graph_directory, exist_ok=True)
                            
                            # Save to JSON file
                            graph_path = os.path.join(
                                graph_directory, 
                                f"{proc_name.lower().replace(' ', '_')}_graph.json"
                            )
                            with open(graph_path, 'w', encoding='utf-8') as f:
                                json.dump(graph_data, f, indent=2, ensure_ascii=False)
                            print(f"→ Saved graph for {proc_name} with {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
                        else:
                            print(f"✗ No valid graph data generated for {proc_name}")
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