from preprocessor import docx_to_markdown_with_docling, process_markdown
from db_handler import DBHandler
from embeddings import process_embeddings
from extractor import ProcedureExtractor
from extractGraphData import extract_nodes_and_edges
import time
import os
import sys
import json

# Add parent directory to path for config import
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from config import Gemini_API_KEY
# from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


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
    output_directory = os.path.join(root_folder, "output")
    graph_directory = os.path.join(root_folder, "graphs")

    try:
        # Initialize database handler
        db_handler = DBHandler(db_path=db_path, persist_directory=persist_directory)
        doc_id = os.path.basename(final_md_path)
        
        # Process markdown and embeddings if needed
        if not os.path.exists(final_md_path):
            print("\n[1/3] Converting DOCX to Markdown...")
            return_code = docx_to_markdown_with_docling(docx_path, temp_md_path)
            if return_code != 0:
                print("✗ Conversion failed. Stopping process.")
                return
            process_markdown(temp_md_path, final_md_path, db_path)
            os.remove(temp_md_path)
            print("\n→ Temporary file cleaned up")
        else:
            print(f"\nUsing existing markdown file: {final_md_path}")
            if not db_handler.get_chunks(doc_id):
                process_markdown(final_md_path, final_md_path, db_path)
            else:
                print("→ Using existing chunks from database")

        # Get or create ChromaDB collection
        collection = process_embeddings(db_handler, doc_id)
        if not collection:
            print("✗ Failed to process embeddings. Stopping.")
            return

        # Extract procedures using Gemini API
        if Gemini_API_KEY:
            procedure_extractor = ProcedureExtractor(api_key=Gemini_API_KEY)
            
            # Define the structured query
            query = """
            Extract structured details specifically for the **Initial Registration** procedure within **Registration Procedures**.
            Ensure the output follows a structured format, capturing the following key fields:

            **Procedure Name:**  
            - "Initial Registration"  

            **Sub-Features to Retrieve:**  
            1. **Triggers:**  
            - Capture key events that cause the UE to initiate the registration procedure.  
            - Include deregistration scenarios and intersystem changes leading to registration.  

            2. **States:**  
            - Extract relevant **5GMM** and **EMM** states before, during, and after registration.  
            - Include conditions for each state transition.  

            3. **Actions:**  
            - List the explicit steps UE takes to initiate registration.  
            - Capture NAS message exchange sequences.  

            4. **Flow of Execution:**  
            - Detail sequential steps in the registration process.  
            - Include key interactions between UE and network.  

            5. **Causes:**  
            - Identify reasons leading to initial registration.  
            - Differentiate between voluntary and network-initiated causes.  

            6. **Expected Outcomes:**  
            - Outline possible successful registration results.  
            - Include GUTI assignment and access to services.  

            7. **Error Handling:**  
            - Capture steps taken when registration fails.  
            - Include scenarios for message rejection and security failures.  

            8. **Feedback Loops:**  
            - Document UE behavior when registration is rejected.  
            - Include mechanisms like retry logic and alternative access methods.  

            **Metadata:**  
            - Constraints & Requirements (if applicable)  
            - Relevant NAS Message Types (e.g., REGISTRATION REQUEST, REGISTRATION ACCEPT, DEREGISTRATION ACCEPT)  
            - References to 3GPP documentation sections.  
            - Extract key excerpts that explain registration initiation conditions.  

            **Instructions for Data Extraction:**  
            - Exclude unrelated MM procedures and background information.  
            - Prioritize accuracy and completeness.  
            - Ensure minimal redundancy while maintaining all essential details.  
        """

            
            os.makedirs(output_directory, exist_ok=True)
            print(f"\nProcessing procedures...")
            
            # Use ChromaDB's semantic search
            results = collection.query(
                query_texts=[query],
                n_results=15,  # Increased for better coverage
                include=["documents", "metadatas", "distances"]
            )
            
            if not results['documents'][0]:
                print("✗ No relevant chunks found")
                return

            # Convert results to chunks format with similarity filtering
            relevant_chunks = []
            for doc, metadata, distance in zip(
                results['documents'][0], 
                results['metadatas'][0],
                results['distances'][0]
            ):
                similarity = 1 - distance
                if similarity >= 0.5:  # Similarity threshold
                    relevant_chunks.append({
                        'title': metadata['title'],
                        'content': doc,
                        'index': metadata['index'],
                        'similarity': similarity
                    })

            if not relevant_chunks:
                print("✗ No chunks met similarity threshold")
                return

            print(f"→ Found {len(relevant_chunks)} relevant chunks")
            
            # Extract procedures from relevant chunks
            procedures = procedure_extractor.extract_procedures_from_query(
                query, relevant_chunks, doc_id
            )
            
            if procedures:
                # Organize procedures by category
                categorized = {}
                for proc in procedures:
                    category = proc['procedure_category']  # Now present
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(proc)

                # Save results by category
                for category, procs in categorized.items():
                    output_path = os.path.join(
                        output_directory, 
                        f"{category.lower().replace(' ', '_')}.json"
                    )
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(procs, f, indent=2, ensure_ascii=False)
                    print(f"→ Saved {len(procs)} {category} procedures to {output_path}")

                    # Extract and store graph data
                    print(f"\nProcessing graph data for {category}...")
                    graph_data = extract_nodes_and_edges(procs, Gemini_API_KEY)
                    
                    if graph_data["nodes"]:
                        # Save to JSON file- optional
                        graph_path = os.path.join(
                            graph_directory, 
                            f"{category.lower().replace(' ', '_')}_graph.json"
                        )
                        with open(graph_path, 'w', encoding='utf-8') as f:
                            json.dump(graph_data, f, indent=2, ensure_ascii=False)
                        print(f"→ Saved graph with {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")

                        # Store in Neo4j
                        # try:
                        #     from extractGraphData import store_in_neo4j
                        #     store_in_neo4j(graph_data, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
                        # except Exception as e:
                        #     print(f"✗ Failed to store in Neo4j: {e}")
                    else:
                        print(f"✗ No graph data generated for {category}")
            else:
                print("✗ No procedures found")
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