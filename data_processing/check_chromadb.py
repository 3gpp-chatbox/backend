import chromadb

client = chromadb.PersistentClient(path="db_3gpp")  # Ensure persistent storage
collection = client.get_or_create_collection("3gpp_specs")
all_data = collection.get()

if all_data["ids"]:
    print(f"Found {len(all_data['ids'])} stored documents in '3gpp_specs'.")
    for doc_id, metadata in zip(all_data["ids"], all_data["metadatas"]):
        print(f"Document ID: {doc_id}")
        print(f"Metadata: {metadata['text'][:200]}...")  # Print the first 200 chars of metadata
else:
    print("No documents found in '3gpp_specs'.")

