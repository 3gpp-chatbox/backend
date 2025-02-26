'''
1.  Purpose: This script is responsible for querying the vector database to retrieve the most relevant text chunks based on a user query and then using an LLM (e.g., Gemini) to extract the 5G NAS procedures from those chunks.

2.  Input:
    *   A user query (string).
    *   The vector database collection object (returned from embeddings.py).
    *   The sentence-transformer model name (same as used in embeddings.py).

3.  Processing:
    *   Queries the vector database for the most similar chunk embeddings
    *   Uses Gemini AI to extract procedures from the chunks
    *   Stores procedure metadata in database
    *   Saves procedure steps in JSON files

4.  Output:
    *   Procedure metadata in database
    *   Procedure steps in JSON files
'''

import google.generativeai as genai
import os
import json
from typing import List, Dict
from db_handler import DBHandler
import chromadb
import time

class ProcedureExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini API and configure the model"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 4096,
        }

    def extract_procedures_from_query(self, query: str, relevant_chunks: List[Dict], doc_title: str) -> List[Dict]:
        """Extract procedures based on query and relevant chunks"""
        prompt = self._create_query_based_prompt(query, relevant_chunks, doc_title)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            if response.text:
                return self._parse_response(response.text, doc_title)
            return []
            
        except Exception as e:
            print(f"Error extracting procedures for query: {e}")
            return []

    def _create_query_based_prompt(self, query: str, chunks: List[Dict], doc_title: str) -> str:
        """Create a prompt that incorporates the query and relevant chunks"""
        chunks_text = "\n\n".join([
            f"Section: {chunk['title']}\nContent: {chunk['content']}"
            for chunk in chunks
        ])
        
        return f"""
    You are a 3GPP specification expert. Extract 5G NAS procedures from the provided context.
    Context:
    {chunks_text}
    Instructions:
    1. Analyze the context and identify {query} NAS procedures.
    2. Format each procedure as a JSON object.
    3. Return a JSON array of all found procedures.
    4. Ensure the output is valid JSON format.

    Required JSON structure for each procedure:
    {{
        "procedure_name": "Name of the procedure",
        "description": "Brief description of procedure's purpose",
        "steps": [
            {{"step_number": 1, "description": "First step description"}},
            {{"step_number": 2, "description": "Second step description"}},
            // ... more steps
        ],
        "related_3gpp_spec_sections": ["Relevant section references"],
        "source_document_title": "{doc_title}",
        "source_chunk_ids": ["List of relevant chunk IDs"]
    }}
    Example response:
    [
        {{
            "procedure_name": "Tracking Area Update (TAU) Procedure",
            "description": "Procedure used by UE to update its location information with the network.",
            "steps": [
                {{"step_number": 1, "description": "UE sends TAU Request to AMF"}},
                {{"step_number": 2, "description": "AMF verifies UE's location and updates its context"}}
            ],
            "related_3gpp_spec_sections": ["TS 24.501 Section 5.3.2"],
            "source_document_title": "{doc_title}",
            "source_chunk_ids": ["0", "1"]
        }}
    ]
    Return ONLY the JSON array. Do not include any additional text or explanations. There can be multiple steps in a procedure.
    """

    def _parse_response(self, response_text: str, doc_title: str) -> List[Dict]:
        """Parse and validate the LLM response"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            if not cleaned_text.startswith('['):
                # Try to find the JSON array in the response
                start_idx = cleaned_text.find('[')
                end_idx = cleaned_text.rfind(']')
                if start_idx != -1 and end_idx != -1:
                    cleaned_text = cleaned_text[start_idx:end_idx + 1]
                else:
                    print("No valid JSON array found in response")
                    return []

            # Parse the JSON
            procedures = json.loads(cleaned_text)
            if not isinstance(procedures, list):
                procedures = [procedures]
            
            # Validate each procedure
            validated_procedures = []
            required_fields = {
                'procedure_name', 'description', 'steps',
                'related_3gpp_spec_sections', 'source_document_title',
                'source_chunk_ids'
            }
            
            for proc in procedures:
                if all(key in proc for key in required_fields):
                    # Ensure steps is properly formatted
                    if isinstance(proc['steps'], list):
                        validated_procedures.append(proc)
                    else:
                        print(f"Invalid steps format in procedure: {proc['procedure_name']}")
            
            return validated_procedures
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text[:200]}...")  # Print first 200 chars for debugging
            return []
        except Exception as e:
            print(f"Error parsing response: {e}")
            return []

def extract_and_store_procedures(db_handler: DBHandler, doc_id: str, api_key: str, query: str, collection: chromadb.Collection):
    """Extract procedures, store metadata in DB and steps in JSON"""
    print("\n[4/4] Extracting relevant procedures...")
    try:
        extractor = ProcedureExtractor(api_key)

        # Search for relevant chunks
        print("Searching for relevant chunks...")
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )
        
        if not results['documents'][0]:
            print("✗ No relevant chunks found")
            return

        print(f"Found {len(results['documents'][0])} relevant chunks")

        # Process results
        chunks = [{
            'title': metadata['title'],
            'content': doc,
            'index': metadata['index']
        } for doc, metadata in zip(results['documents'][0], results['metadatas'][0])]

        # Extract procedures
        print("\nExtracting procedures using Gemini AI...")
        doc_title = f"3GPP TS {doc_id.split('.')[0]}"
        procedures = extractor.extract_procedures_from_query(query, chunks, doc_title)
        
        if procedures:
            # Create output directory for steps
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "procedures", doc_id)
            os.makedirs(output_dir, exist_ok=True)
            
            similarity_score = 1 - results['distances'][0][0]
            
            # Store each procedure's metadata in DB and steps in JSON
            for i, procedure in enumerate(procedures):
                # Save steps to JSON file
                steps_file = os.path.join(output_dir, f"procedure_{i+1}_steps.json")
                steps_data = {
                    "procedure_name": procedure['procedure_name'],
                    "steps": procedure['steps']
                }
                
                with open(steps_file, 'w', encoding='utf-8') as f:
                    json.dump(steps_data, f, indent=2, ensure_ascii=False)
                
                # Store metadata in database
                db_handler.store_procedure_metadata({
                    "procedure_name": procedure['procedure_name'],
                    "description": procedure['description'],
                    "steps_file": steps_file,
                    "related_3gpp_spec_sections": procedure['related_3gpp_spec_sections'],
                    "source_document_title": procedure['source_document_title'],
                    "source_chunk_ids": procedure['source_chunk_ids'],
                    "doc_id": doc_id,
                    "similarity_score": similarity_score
                })
            
            print(f"✓ Successfully processed {len(procedures)} procedures:")
            print(f"  - Metadata stored in database")
            print(f"  - Steps saved in: {output_dir}")
        else:
            print("✗ No relevant procedures found")

    except Exception as e:
        print(f"✗ Error during extraction: {e}")