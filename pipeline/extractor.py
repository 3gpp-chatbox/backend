import google.generativeai as genai
import os
import json
from typing import List, Dict, Optional
from typing import Any
from db_handler import DBHandler
import chromadb
from pydantic import BaseModel, Field
from google import genai

# Pydantic models for validation
class ProcedureFeature(BaseModel):
    feature_name: str
    description: str

class Procedure(BaseModel):
    procedure_name: str
    procedure_category: str = Field(..., description="Main category (Registration, Deregistration, TAU, or Handover)")
    sub_category: Optional[str] = Field(None, description="Specific type under the main category")
    trigger: str
    state: str
    causes: List[str]
    expected_outcomes: List[str]
    error_handling: Optional[str]
    related_3gpp_spec_sections: List[str]
    message_types: List[str]
    source_document_title: str
    source_chunk_ids: List[str]
    similarity_score: float

class ExtractionResponse(BaseModel):
    procedures: List[Procedure]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProcedureExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini API and configure the model"""
        self.client=genai.Client(api_key=api_key)
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "response_mime_type": "application/json",
            "response_schema":Procedure
            # "max_output_tokens": 8000,
        }
        # genai.configure(api_key=api_key)
        # self.model = genai.GenerativeModel(model_name)
        # self.generation_config = {
        #     "temperature": 0.2,
        #     "top_p": 0.8,
        #     "top_k": 40,
        #     "max_output_tokens": 8000,
        # }

    def extract_procedures_from_query(self, query: str, relevant_chunks: List[Dict], doc_title: str) -> List[Dict]:
        """Extract procedures based on query and relevant chunks"""
        prompt = self._create_query_based_prompt(query, relevant_chunks, doc_title)
        
        try:
            response = self.client.models.generate_content(
                model= "gemini-2.0-flash",
                contents=prompt,
                config=self.generation_config
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
            f"Section {chunk['title']}\nContent: {chunk['content']}"
            for chunk in chunks
        ])
        
        return f"""You are a 3GPP specification expert. Extract 5G NAS procedure features from the provided context.

Context:
{chunks_text}

Instructions:
{query}

Return each procedure as a JSON object with this structure:
{{
    "procedure_name": "Name of the procedure",
    "procedure_category": "One of: Registration, Deregistration, TAU, or Handover",
    "sub_category": "Specific type (e.g., 'Initial Registration') or null",
    "trigger": "What initiates this procedure",
    "state": "State of the UE/network during execution",
    "causes": ["Reasons why this procedure occurs"],
    "expected_outcomes": ["Expected results"],
    "error_handling": "How errors are handled",
    "related_3gpp_spec_sections": ["Relevant section numbers"],
    "message_types": ["Messages used in this procedure"],
    "source_document_title": "{doc_title}",
    "source_chunk_ids": ["Relevant chunk IDs"],
    "similarity_score": "Similarity score between 0 and 1"
}}

IMPORTANT:
- Return ONLY valid JSON
- Include all fields
- Use proper JSON formatting with double quotes
- Set procedure_category to one of the specified categories
- Skip procedures that don't fit the categories
"""

    def _parse_response(self, response_text: str, doc_title: str) -> List[Dict]:
        """Parse and validate the LLM response"""
        try:
            cleaned_text = response_text.strip()
            
            # Handle both array and single object responses
            if cleaned_text.startswith('{'):
                # Single object response - convert to array
                procedures = [json.loads(cleaned_text)]
            elif cleaned_text.startswith('['):
                # Array response
                procedures = json.loads(cleaned_text)
            else:
                # Try to find JSON content
                start_idx = cleaned_text.find('{')
                end_idx = cleaned_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    cleaned_json = cleaned_text[start_idx:end_idx + 1]
                    procedures = [json.loads(cleaned_json)]
                else:
                    print("No valid JSON found in response")
                    return []

            # Ensure procedures is a list
            if not isinstance(procedures, list):
                procedures = [procedures]
            
            # Validate each procedure
            validated_procedures = []
            for proc in procedures:
                try:
                    # Add source document if missing
                    if 'source_document_title' not in proc:
                        proc['source_document_title'] = doc_title
                    
                    # Validate against Pydantic model
                    validated_proc = Procedure(**proc)
                    validated_procedures.append(validated_proc)
                except Exception as e:
                    print(f"Error validating procedure: {e}")
                    continue
            
            return validated_procedures
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text[:200]}...")
            return []
        except Exception as e:
            print(f"Error parsing response: {e}")
            print(f"Response text: {response_text[:200]}...")
            return []

    def perform_similarity_search(
        collection: chromadb.Collection,
        query: str,
        doc_id: Optional[str] = None,
        n_results: int = 8,
        similarity_threshold: float = 0.65
    ) -> List[Dict]:
        """Perform vector similarity search on the collection"""
        
        # Execute similarity search
        search_results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
            where={"doc_id": doc_id} if doc_id else None,
        )
        
        # Process and filter results
        similar_chunks = []
        total_context = 0
        max_context = 8000
        
        for doc, metadata, distance in zip(
            search_results['documents'][0],
            search_results['metadatas'][0],
            search_results['distances'][0]
        ):
            similarity = 1 - distance
            
            if similarity >= similarity_threshold:
                chunk = {
                    'title': metadata['title'],
                    'content': doc,
                    'index': metadata['index'],
                    'similarity': similarity
                }
                
                if total_context + len(doc) <= max_context:
                    similar_chunks.append(chunk)
                    total_context += len(doc)
                else:
                    break
        
        return similar_chunks

    def extract_procedures(self, query: str, api_key: str, collection: chromadb.Collection, doc_id: Optional[str] = None) -> ExtractionResponse:
        """Extract procedures using vector similarity search"""
        print("\n[4/4] Extracting relevant procedures...")
        try:
            similar_chunks = self.perform_similarity_search(
                collection=collection,
                query=query,
                doc_id=doc_id,
                n_results=8,
                similarity_threshold=0.65
            )
            
            if not similar_chunks:
                return ExtractionResponse(
                    procedures=[], 
                    metadata={"error": "No similar chunks found"}
                )

            # Process similarity search results
            similarity_threshold = 0.65
            chunks = []
            total_context = 0
            max_context = 10000

            # Convert distances to similarities and filter
            for chunk in similar_chunks:
                similarity = chunk['similarity']
                
                if similarity >= similarity_threshold:
                    chunks.append(chunk)
                    total_context += len(chunk['content'])
                    if total_context > max_context:
                        break

            if not chunks:
                return ExtractionResponse(
                    procedures=[], 
                    metadata={"error": "No valid chunks found"}
                )
        except Exception as e:
            print(f"Error extracting procedures: {e}")
            return ExtractionResponse(
                procedures=[], 
                metadata={"error": str(e)}
            )
