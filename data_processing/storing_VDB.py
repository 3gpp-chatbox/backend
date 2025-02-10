import chromadb
from sentence_transformers import SentenceTransformer
from preprocessing import extract_text_from_pdf, save_text_chunks
import os
import hashlib  # For generating unique IDs

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="db_3gpp")
collection = chroma_client.get_or_create_collection(name="3gpp_specs")

# Get text chunks
pdf_file = os.path.join(os.path.dirname(__file__), "..", "data_store", "TS 24.234.pdf")

if os.path.exists(pdf_file):
    raw_text = extract_text_from_pdf(pdf_file)
    chunks = save_text_chunks(raw_text)
    
    # Fetch existing document IDs to prevent duplication
    existing_docs = collection.get()["ids"]
    
    # Insert document chunks (only if not already in DB)
    for chunk in chunks:
        chunk_id = hashlib.md5(chunk.encode()).hexdigest()  # Unique ID for the text chunk
        
        if chunk_id not in existing_docs:  # Avoid duplicates
            embedding = model.encode(chunk).tolist()
            collection.add(ids=[chunk_id], embeddings=[embedding], metadatas=[{"text": chunk}])
            print(f"added chunk id: {chunk_id}")
    
    print("New document chunks stored successfully!")
else:
    print(f"PDF file not found: {pdf_file}")

# Fetch all stored documents
documents = collection.get()

# Print the stored metadata (text chunks)
for doc_id, metadata in zip(documents["ids"], documents["metadatas"]):
    print(f"ID: {doc_id}, Text: {metadata['text'][:200]}...")  # Print first 200 chars
