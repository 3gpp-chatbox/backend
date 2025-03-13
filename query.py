import chromadb
from sentence_transformers import SentenceTransformer

# Initialize the Chroma client
client = chromadb.PersistentClient(path="./chroma_db")  # Specify the path to the Chroma database

# Get the collection (assuming your collection is named 'sections')
collection = client.get_collection("sections")  # This should match the name of your collection

# Load a pre-trained model to generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# The section name we want to search for
section_name_query = "initial registration initiation"

# Generate embedding for the query text (section name)
query_embedding = model.encode([section_name_query])[0]  # Single query, so we access the first item

# Perform the query on the collection with embeddings and metadata
results = collection.query(
    query_embeddings=[query_embedding],  # Embedding generated from section name
    n_results=5,  # Number of results to return
    where={"section_name": section_name_query}  # Filter by section name (metadata)
)

# Print the structure of results to inspect it
print("Query Results Structure:")
print(results)

# Assuming results['documents'] is a list of lists, access each document
if results['documents']:
    for doc_list in results['documents']:
        for doc in doc_list:
            # Access the document content and metadata based on your collection structure
            print("Section ID:", doc.get('section_id', 'N/A'))
            print("Section Name:", doc.get('section_name', 'N/A'))
            print("Content:", doc.get('content_chunk', 'No content available'))
else:
    print(f"No results found for section name: {section_name_query}")
