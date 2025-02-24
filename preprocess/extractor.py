'''
use LLM-Based Extraction
- use Gemini API with suitable model, temperature
- use prompt to extract the information
- calculate the similarity between the extracted data and the queries by semantic search using embeddings
- pass the data chunks with embeddings that are "close" (in terms of cosine similarity or other distance metrics) to the query embedding to the LLM to extract the procedures
- store the procedures in a database

'''

import google.generativeai as genai
import sqlite3
import os
import json
from typing import List, Dict, Tuple
from db_handler import ChunkDBHandler
from embeddings import EmbeddingHandler

class ProcedureExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """Initialize Gemini API and configure the model"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = {
            "temperature": 0.2,  # Lower temperature for more structured output
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
        Based on the following query and context, extract specific procedures and technical details.
        
        Query: {query}

        Context:
        {chunks_text}

        For each extracted procedure, provide the following information in JSON format:

        {{
        "procedure_name": "Name of the NAS procedure (e.g., Registration, PDU Session Establishment)",
        "description": "A brief description of the procedure's purpose.",
        "steps": [
            {{"step_number": 1, "description": "Detailed description of step 1"}},
            {{"step_number": 2, "description": "Detailed description of step 2"}}
        ],
        "related_3gpp_spec_sections": ["List of relevant 3GPP specification sections"],
        "source_document_title": "{doc_title}",
        "source_chunk_ids": ["List of chunk IDs used to extract this procedure"]
        }}

        Return a JSON array containing the extracted procedures. If no 5G NAS procedures are found, return an empty JSON array.

        Example:
        [
        {{
            "procedure_name": "Registration",
            "description": "The UE registers with the 5G core network.",
            "steps": [
            {{"step_number": 1, "description": "The UE sends a Registration Request message."}}
            ],
            "related_3gpp_spec_sections": ["3GPP TS 23.502 Section 4.2.2"],
            "source_document_title": "3GPP_TS_23_502.docx",
            "source_chunk_ids": ["chunk_123", "chunk_124"]
        }}
        ]
        """

    def _parse_response(self, response_text: str, doc_title: str) -> List[Dict]:
        """Parse and validate the LLM response"""
        try:
            procedures = json.loads(response_text)
            if not isinstance(procedures, list):
                procedures = [procedures]
            
            # Validate each procedure has required fields
            validated_procedures = []
            for proc in procedures:
                if all(key in proc for key in [
                    'procedure_name', 'description', 'steps',
                    'related_3gpp_spec_sections', 'source_document_title',
                    'source_chunk_ids'
                ]):
                    validated_procedures.append(proc)
            
            return validated_procedures
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

def extract_and_store_procedures(db_path: str, doc_id: str, api_key: str, query: str, index_path: str):
    """Main function to extract and store procedures based on semantic search"""
    print("\n[4/4] Extracting relevant procedures...")
    try:
        # Initialize handlers
        chunk_db = ChunkDBHandler(db_path)
        procedure_db = ProcedureDB(db_path)
        extractor = ProcedureExtractor(api_key)
        embedding_handler = EmbeddingHandler()

        # Load the saved index
        print("→ Loading embeddings index...")
        embedding_handler.load_index(index_path)

        # Perform semantic search
        print(f"→ Searching for chunks relevant to: {query}")
        similar_chunks = embedding_handler.search(query, k=5)  # Get top 5 relevant chunks
        
        if not similar_chunks:
            print("No relevant chunks found")
            return

        # Get full chunk data for relevant chunks
        chunks = chunk_db.get_chunks(doc_id)
        relevant_chunks = [
            chunks[chunk_id] for chunk_id, similarity in similar_chunks
            if chunk_id < len(chunks)
        ]

        # Extract procedures from relevant chunks
        print("→ Extracting NAS procedures from relevant chunks...")
        doc_title = f"3GPP TS {doc_id.split('.')[0]}"  # Format document title
        procedures = extractor.extract_procedures_from_query(query, relevant_chunks, doc_title)
        
        if procedures:
            # Store with best similarity score
            best_similarity = similar_chunks[0][1] if similar_chunks else 0
            procedure_db.store_nas_procedure(procedures, doc_id, best_similarity)
            print(f"✓ Extracted and stored {len(procedures)} NAS procedures")
        else:
            print("No relevant NAS procedures found in the chunks")

    except Exception as e:
        print(f"✗ Error during procedure extraction: {e}")