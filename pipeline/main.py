from preprocessor import docx_to_markdown_with_docling, process_markdown
from db_handler import DBHandler
from embeddings import process_embeddings
from extractor import extract_and_store_procedures
import time
import os
import sys

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

    try:
        # Initialize database handler
        db_handler = DBHandler(db_path=db_path, persist_directory=persist_directory)
        doc_id = os.path.basename(final_md_path)
        
        # Check if markdown exists and process if needed
        if not os.path.exists(final_md_path):
            print("\n[1/3] Converting DOCX to Markdown...")
            return_code = docx_to_markdown_with_docling(docx_path, temp_md_path)
            
            if return_code != 0:
                print("✗ Conversion failed. Stopping process.")
                return

            process_markdown(temp_md_path, final_md_path, db_path)
            
            if os.path.exists(temp_md_path):
                os.remove(temp_md_path)
                print("\n→ Temporary file cleaned up")
        else:
            print(f"\nUsing existing markdown file: {final_md_path}")
            # Only process markdown if no chunks exist
            if not db_handler.get_chunks(doc_id):
                process_markdown(final_md_path, final_md_path, db_path)
            else:
                print("→ Using existing chunks from database")

        # Process embeddings (will reuse if they exist)
        collection = process_embeddings(db_handler, doc_id)
        if not collection:
            print("✗ Failed to process embeddings. Stopping.")
            return

        # Extract procedures
        if Gemini_API_KEY:
            query = """Mobility Management (MM) Registration"""
            extract_and_store_procedures(db_handler, doc_id, Gemini_API_KEY, query, collection)
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