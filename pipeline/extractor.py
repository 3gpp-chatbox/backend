import google.generativeai as genai
import os
import json
from typing import List, Dict, Optional, Any
import chromadb
from pydantic import BaseModel, Field, ValidationError

# Define Pydantic models
class SubFeatures(BaseModel):
    Triggers: List[str] = Field(
        ...,
        description="Triggers causing transitions between states."
    )
    States: List[str] = Field(
        ...,
        description="Different conditions or statuses of the UE and network elements."
    )
    Actions: List[str] = Field(
        ...,
        description="Actions taken by the UE and network elements."
    )
    Flow_of_execution: List[str] = Field(
        ...,
        description="Sequence of steps in the procedure"
    )
    Causes: List[str] = Field(
        ...,
        description="Cause of the procedure"
    )   
    Expected_Outcomes: List[str] = Field(
        ...,
        description="Expected outcomes of the procedure"
    )
    Error_Handling: List[str] = Field(
        ...,
        description="Error handling for the procedure"
    )
    Feedback_Loops: List[str] = Field(
        ...,
        description="Feedback loops for the procedure"
    )

class Metadata(BaseModel):
    Constraints_Requirements: Optional[str] = Field(
        None, 
        description="Network availability, resource allocation"
    )
    Message_Types: Optional[str] = Field(
        None,
        description="Types of messages exchanged during the procedure"
    )
    References: Optional[str] = Field(
        None,
        description="relevant document name and section titles of the given context"
    )
    Excerpts: Optional[str] = Field(
        None,
        description="Direct quotes from the given context"
    )
    Identifiers: Optional[str] = Field(
        None,
        description="Unique procedure IDs"
    )

class Procedure(BaseModel):
    procedure_name: str 
    sub_features: SubFeatures
    metadata: Metadata

class ProcedureCategory(BaseModel):
    category_name: str 
    procedures: List[Procedure]

class ProceduresSchema(BaseModel):
    level_1_procedures: List[ProcedureCategory]

class ExtractionResponse(BaseModel):
    procedures: List[Procedure]
    metadata: Dict[str, Any]

class ProcedureExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini API and configure the model"""
        genai.configure(api_key=api_key) 
        self.client = genai.GenerativeModel(model_name)
        self.generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            # "max_output_tokens": 8000
        }

    def extract_procedures_from_query(self, query: str, relevant_chunks: List[Dict], doc_title: str) -> List[Procedure]:
        """Extract procedures based on query and relevant chunks"""
        prompt = self._create_query_based_prompt(query, relevant_chunks, doc_title)
        
        try:
            response = self.client.generate_content(
                contents=prompt,
                generation_config=self.generation_config
            )

        # Log token usage
            if hasattr(response, 'candidates'):
                print(f"\nToken usage:")
                print(f"Total tokens: {response.candidates[0].token_count}")
                
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
        
        # Use model_json_schema 
        schema = json.dumps(ProceduresSchema.model_json_schema(), indent=2)
        
        return f"""
        You are a 3GPP specification expert. Your task is to analyze the provided 
        {query} procedure taxonomy and metadata structure and generate a JSON representation of it.  
        The JSON should capture the hierarchical relationships between categories, procedures, and their sub-features,
        as well as incorporate the metadata elements.
        Context: {chunks_text}
        document: {doc_title}
        **Output Format (Valid JSON Schema)**:
        {schema}
        1. Ensure the output is valid JSON and follows the above schema.
        2. **All information must be derived exclusively from the provided context.**
        3. Ensure all references point to **only** the given context.
        4. For the `sub_features` section, provide short content of the triggers, states, causes, expected outcomes, error handling, and feedback loops.
        5. Don't include excessive direct references to specific sections within `sub_features` section.
        **Do not generate information from your pre-existing knowledge.**
        """

    def _parse_response(self, response_text: str, doc_title: str) -> List[Dict]:
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]

            data = json.loads(cleaned_text.strip())
            validated_data = ProceduresSchema(**data)
            
            procedures_list = []
            for category in validated_data.level_1_procedures:
                for procedure in category.procedures:
                    procedure_dict = procedure.dict()
                    procedure_dict['procedure_category'] = category.category_name  # Add category dynamically
                    procedures_list.append(procedure_dict)

            print(f"Successfully parsed {len(procedures_list)} procedures")
            return procedures_list
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text[:200]}...")
            return []
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []


    def perform_similarity_search(
        self,
        collection: chromadb.Collection,
        query: str,
        doc_id: Optional[str] = None,
        n_results: int = 10,
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
        max_context = 10000
        
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

    def extract_procedures(self, query: str, collection: chromadb.Collection, doc_id: Optional[str] = None) -> ExtractionResponse:
        """Extract procedures using vector similarity search and process results"""
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
            total_context = 0
            max_context = 10000
            chunks = []

            for chunk in similar_chunks:
                if total_context + len(chunk['content']) > max_context:
                    break
                chunks.append(chunk)
                total_context += len(chunk['content'])

            if not chunks:
                return ExtractionResponse(
                    procedures=[], 
                    metadata={"error": "No valid chunks found"}
                )

            extracted_procedures = self.extract_procedures_from_query(query, chunks, doc_id)
            return ExtractionResponse(procedures=extracted_procedures, metadata={"source": doc_id})
        
        except Exception as e:
            print(f"Error extracting procedures: {e}")
            return ExtractionResponse(procedures=[], metadata={"error": str(e)})

