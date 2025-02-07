from preprocess_pdfs import read_pdfs_from_directory
from store_data_chroma import store_documents_in_chroma, check_if_documents_exist
from query_data import query_documents

def main():
    # Step 1: Check if documents are already in ChromaDB
    print("📂 Checking ChromaDB for existing documents...")
    documents_in_db = check_if_documents_exist()

    if not documents_in_db:
        print("📂 Reading PDFs...")
        data_directory = "data"
        documents = read_pdfs_from_directory(data_directory)
        print(f"✅ Found {len(documents)} documents")

        if not documents:
            print("❌ No documents found. Check the data folder.")
            return

        # Step 2: Store in ChromaDB
        print("\n💾 Storing documents in ChromaDB...")
        vector_store = store_documents_in_chroma(documents)

        if not vector_store:
            print("❌ Storing failed. Check errors above.")
            return
    else:
        print("✅ Documents already stored in ChromaDB, skipping PDF read.")

    # Step 3: Test Queries
    test_queries = [
        "What is the main topic?",
        "Explain 3GPP NAS procedures",
    ]

    print("\n🔎 Testing queries...")
    for query in test_queries:
        results = query_documents(query)
        print(f"\nQuery: {query}")
        print("Top 3 results:")
        for i, result in enumerate(results[:3], 1):
            print(f"\n{i}. Source: {result['metadata']['source']}")
            print(f"Distance: {result['distance']}")
            print(f"Text snippet: {result['text'][:200]}...")

if __name__ == "__main__":
    main()
