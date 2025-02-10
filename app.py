import os
from dotenv import load_dotenv
from preprocess_pdfs import read_pdfs_from_directory
from store_data_chroma import store_documents_in_chroma, check_if_documents_exist  # Import from store_data_chroma.py
from store_data_neo4j import store_in_neo4j, KnowledgeGraph  # Import from store_data_neo4j.py
from query_data import query_documents
from typing import List, Tuple

# Load environment variables from .env file
load_dotenv()

# Neo4j Configuration (from environment variables)
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def check_if_entities_exist_in_neo4j() -> bool:
    """Check if entities already exist in Neo4j."""
    graph = KnowledgeGraph(URI, USERNAME, PASSWORD)
    with graph.driver.session() as session:
        result = session.run("MATCH (n:Entity) RETURN n LIMIT 1")
        return bool(result.single())

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

    # Step 3: Check if entities already exist in Neo4j
    print("🧠 Checking Neo4j for existing entities...")
    if not check_if_entities_exist_in_neo4j():
        print("📂 Storing entities and relationships in Neo4j...")
        store_in_neo4j(documents)
        print("✅ Data successfully stored in Neo4j!")
    else:
        print("✅ Entities already stored in Neo4j, skipping.")

    # Step 4: Test Queries
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
