from nas_graph_extractor import GraphExtractor
from docx import Document
import os

def main():
    base_dir = "../3GPP_Documents"
    spec_dir = os.path.join(base_dir, "TS_24_501")
    
    if not os.path.exists(spec_dir):
        print(f"Directory {spec_dir} does not exist")
        return
        
    docx_files = [f for f in os.listdir(spec_dir) if f.endswith('.docx')]
    
    if not docx_files:
        print(f"No .docx file found in {spec_dir}")
        return
        
    docx_path = os.path.join(spec_dir, docx_files[0])
    print(f"Processing document: {docx_path}")
    
    try:
        # Extract text from the document
        doc = Document(docx_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        # Create the GraphExtractor instance
        # Optionally, specify a different DB path if desired
        extractor = GraphExtractor(db_path="nas_chunks.db")
        
        # Process text in chunks; results are stored in a local SQLite DB
        nodes, edges = extractor.process_text_in_chunks(text)
        
        # Display aggregated results
        extractor.print_graph_summary()
        
    except Exception as e:
        print(f"Error processing document: {str(e)}")

if __name__ == "__main__":
    main()
