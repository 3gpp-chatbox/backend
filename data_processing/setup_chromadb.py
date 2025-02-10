import chromadb
from chromadb.config import Settings

# Correctly set up ChromaDB client
client = chromadb.Client()

# Check for available collections
collections = client.list_collections()
print("Collections:", collections)
