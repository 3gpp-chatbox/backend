from preprocessor import docx_to_markdown_with_docling, process_markdown
from db_handler import ChunkDBHandler
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
    
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docx_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.docx")
    temp_md_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "temp.md")
    final_md_path = os.path.join(root_folder, "3GPP_Documents", "TS_24_501", "24501-j11.md")
    db_path = os.path.join(root_folder, "3GPP_Documents", "chunks.db")
    index_path = os.path.join(root_folder, "3GPP_Documents", "embeddings.index")

    try:
        # Initialize database
        db_handler = ChunkDBHandler(db_path)
        
        # Check if final markdown exists
        if not os.path.exists(final_md_path):
            print("\n[1/2] Converting DOCX to Markdown...")
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
            process_markdown(final_md_path, final_md_path, db_path)

        # Create or load embeddings
        doc_id = os.path.basename(final_md_path)
        embeddings_success = process_embeddings(db_path, doc_id, index_path)
        
        if not embeddings_success:
            print("✗ Failed to process embeddings. Stopping.")
            return

        # Extract procedures using API key directly from config
        if Gemini_API_KEY:
            query = """
Extract 5G-related Non-Access Stratum (NAS) procedures from the provided context. 
A 5G NAS procedure is a sequence of steps performed by a User Equipment (UE) and the 5G core network 
to manage mobility, session management, and other functions related to 5G connectivity. 
Focus on procedures that involve signaling between the UE and the network. 
Exclude procedures related to radio access network (RAN) or other access technologies.

Look for procedures such as:
1. Registration procedures
2. Authentication procedures
3. Security procedures
4. Session management procedures
5. Mobility management procedures
"""
            extract_and_store_procedures(db_path, doc_id, Gemini_API_KEY, query, index_path)
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