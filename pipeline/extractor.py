'''
1.  Purpose: This script is responsible for querying the vector database to retrieve the most relevant text chunks based on a user query and then using an LLM (e.g., Gemini) to extract the 5G NAS procedures from those chunks.

2.  Input:
    *   A user query (string).
    *   The vector database collection object (returned from embeddings.py).
    *   The sentence-transformer model name (same as used in embeddings.py, default is `all-mpnet-base-v2`).

3.  Processing:
    *   Loads the same sentence-transformer model used in `embeddings.py`.
    *   Creates an embedding for the user query.
    *   Queries the vector database for the most similar chunk embeddings (and their metadata, including the text chunks).
    *   Constructs a prompt for the LLM, including the user query and the retrieved text chunks.
    *   Calls the Gemini API (or your chosen LLM API) with the prompt.
    *   use LLM to cluster the response
    *   Parses the LLM response to extract the procedures.

4.  Output:
    *   The extracted 5G NAS procedures in json format.

'''

import google.generativeai as genai
import sqlite3
import os
import json
from typing import List, Dict, Tuple
from db_handler import ChunkDBHandler, DBHandler
from embeddings import EmbeddingHandler
import chromadb

class ProcedureExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
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
        
        return f"""You are a 3GPP specification expert. Extract 5G NAS procedures from the provided context.
        
Query: {query}

Context:
{chunks_text}

Instructions:
1. Analyze the context and identify NAS procedures
2. Format each procedure as a JSON object
3. Return a JSON array of all found procedures
4. Ensure the output is valid JSON format

Required JSON structure for each procedure:
{{
    "procedure_name": "Name of the NAS procedure",
    "description": "Brief description of the procedure's purpose",
    "steps": [
        {{"step_number": 1, "description": "First step description"}},
        {{"step_number": 2, "description": "Second step description"}},
        ....... (more steps can be added)
    ],
    "related_3gpp_spec_sections": ["Relevant section references"],
    "source_document_title": "{doc_title}",
    "source_chunk_ids": ["List of relevant chunk IDs"]
}}

Example response:
[
    {{
        "procedure_name": "Initial Registration Procedure",
        "description": "Procedure used by UE to register with the 5G network for the first time",
        "steps": [
            {{"step_number": 1, "description": "UE sends Registration Request to AMF"}},
            {{"step_number": 2, "description": "AMF initiates authentication procedure"}}
        ],
        "related_3gpp_spec_sections": ["TS 24.501 Section 5.5.1.2"],
        "source_document_title": "{doc_title}",
        "source_chunk_ids": ["0", "1"]
    }}
]

Return ONLY the JSON array. Do not include any additional text or explanations."""

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

class ProcedureDB:
    def __init__(self, db_path: str):
        """Initialize the procedures database"""
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Create the procedures table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nas_procedures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    procedure_name TEXT,
                    description TEXT,
                    steps JSON,  -- Store steps as JSON array
                    related_3gpp_spec_sections JSON,  -- Store sections as JSON array
                    source_document_title TEXT,
                    source_chunk_ids JSON,  -- Store chunk IDs as JSON array
                    doc_id TEXT,
                    similarity_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def store_nas_procedure(self, procedures: List[Dict], doc_id: str, similarity_score: float):
        """Store extracted NAS procedures in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for procedure in procedures:
                cursor.execute('''
                    INSERT INTO nas_procedures (
                        procedure_name, description, steps, 
                        related_3gpp_spec_sections, source_document_title,
                        source_chunk_ids, doc_id, similarity_score
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    procedure['procedure_name'],
                    procedure['description'],
                    json.dumps(procedure['steps']),
                    json.dumps(procedure['related_3gpp_spec_sections']),
                    procedure['source_document_title'],
                    json.dumps(procedure['source_chunk_ids']),
                    doc_id,
                    similarity_score
                ))
            conn.commit()

def extract_and_store_procedures(db_handler: DBHandler, doc_id: str, api_key: str, query: str, collection: chromadb.Collection):
    """Extract and store procedures"""
    print("\n[4/4] Extracting relevant procedures...")
    try:
        extractor = ProcedureExtractor(api_key)

        # Search for relevant chunks
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents", "metadatas", "distances"]
        )
        
        if not results['documents'][0]:
            print("No relevant chunks found")
            return

        # Process results
        chunks = [{
            'title': metadata['title'],
            'content': doc,
            'index': metadata['index']
        } for doc, metadata in zip(results['documents'][0], results['metadatas'][0])]

        # Extract and store procedures
        doc_title = f"3GPP TS {doc_id.split('.')[0]}"
        procedures = extractor.extract_procedures_from_query(query, chunks, doc_title)
        
        if procedures:
            similarity_score = 1 - results['distances'][0][0]
            db_handler.store_procedures(procedures, doc_id, similarity_score)
            print(f"✓ Extracted and stored {len(procedures)} procedures")
        else:
            print("No relevant procedures found")

    except Exception as e:
        print(f"✗ Error during extraction: {e}")