import chromadb
from sentence_transformers import SentenceTransformer
from preprocessing import extract_text_from_pdf, save_text_chunks
import os

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="3gpp_db")
collection = chroma_client.get_or_create_collection(name="3gpp_specs")

# Get text chunks
pdf_file = os.path.join(os.path.dirname(__file__), "..", "data", "TS 24.234.pdf")
if os.path.exists(pdf_file):
    raw_text = extract_text_from_pdf(pdf_file)
    chunks = save_text_chunks(raw_text)
    
    # Insert document chunks
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(ids=[str(i)], embeddings=[embedding], metadatas=[{"text": chunk}])
    
    print("Documents stored successfully!")
else:
    print(f"PDF file not found: {pdf_file}")
