from preprocessor import docx_to_markdown_with_docling, process_markdown
from db_handler import DBHandler
from embeddings import process_embeddings
from extractor import ProcedureExtractor
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
    temp_md_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "temp.md")
    final_md_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.md")
    db_path = os.path.join(root_folder, "DB", "chunks.db")
    persist_directory = os.path.join(root_folder, "DB", "chroma_db")
    output_directory = os.path.join(root_folder, "output")

    try:
        # Initialize database handler
        db_handler = DBHandler(db_path=db_path, persist_directory=persist_directory)
        doc_id = os.path.basename(final_md_path)
        
        # Process markdown and embeddings if needed
        if not os.path.exists(final_md_path):
            print("\n[1/3] Converting DOCX to Markdown...")
            return_code = docx_to_markdown_with_docling(docx_path, temp_md_path)
            if return_code != 0:
                print("✗ Conversion failed. Stopping process.")
                return
            process_markdown(temp_md_path, final_md_path, db_path)
            os.remove(temp_md_path)
            print("\n→ Temporary file cleaned up")
        else:
            print(f"\nUsing existing markdown file: {final_md_path}")
            if not db_handler.get_chunks(doc_id):
                process_markdown(final_md_path, final_md_path, db_path)
            else:
                print("→ Using existing chunks from database")

        # Get or create ChromaDB collection
        collection = process_embeddings(db_handler, doc_id)
        if not collection:
            print("✗ Failed to process embeddings. Stopping.")
            return

        # Extract procedures using Gemini API
        if Gemini_API_KEY:
            procedure_extractor = ProcedureExtractor(api_key=Gemini_API_KEY)
            queries = [
                "Mobility Management (MM) Registration- Initial Registration",
                "Mobility Management (MM) Registration- Periodic Registration",
                "Mobility Management (MM) Registration- Mobility Registration",
            ]
            
            os.makedirs(output_directory, exist_ok=True)
            
            for query in queries:
                print(f"\nProcessing query: {query}")
                
                # Use ChromaDB's semantic search
                results = collection.query(
                    query_texts=[query],
                    n_results=10,  # Increased for better coverage
                    include=["documents", "metadatas", "distances"]
                )
                
                if not results['documents'][0]:
                    print(f"✗ No relevant chunks found for query: {query}")
                    continue

                # Convert results to chunks format
                relevant_chunks = []
                for doc, metadata, distance in zip(
                    results['documents'][0], 
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    # Only include chunks with good similarity
                    similarity = 1 - distance 
                    if similarity >= 0.5:  # Adjust threshold as needed
                        relevant_chunks.append({
                            'title': metadata['title'],
                            'content': doc,
                            'index': metadata['index'],
                            'similarity': similarity
                        })

                if not relevant_chunks:
                    print(f"✗ No chunks met similarity threshold for query: {query}")
                    continue

                print(f"→ Found {len(relevant_chunks)} relevant chunks")
                
                # Extract procedures from relevant chunks
                response = procedure_extractor.extract_procedures_from_query(
                    query, relevant_chunks, doc_id
                )
                
                if response:
                    # Save results
                    output_path = os.path.join(
                        output_directory, 
                        f"{query.lower().replace(' ', '_').replace('(', '').replace(')', '')}.json"
                    )
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump([proc.dict() for proc in response], f, indent=2, ensure_ascii=False)
                    print(f"→ Results saved to {output_path}")
                    print(f"✓ Found {len(response)} procedures")
                else:
                    print(f"✗ No procedures found for query: {query}")
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