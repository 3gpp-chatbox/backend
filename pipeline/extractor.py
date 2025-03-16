import google.generativeai as genai
import json
from typing import List, Dict, Optional, Any
import chromadb
from pydantic import BaseModel, Field, ValidationError

# Define Pydantic models for property graph
class Properties(BaseModel):
    description: str = Field(..., description="Description of the node or edge")
    actor: Optional[str] = Field(None, description="Actor involved (UE or Network)")
    reference: str = Field(..., description="Reference to the 3GPP specification section")
    conditions: Optional[List[str]] = Field(None, description="Conditions that must be met")
    timers: Optional[List[str]] = Field(None, description="Timers affecting this element")
    messages: Optional[List[str]] = Field(None, description="NAS messages involved")

class Node(BaseModel):
    id: str = Field(..., description="Unique identifier for the node")
    type: str = Field(..., description="Node type (state, event, message)")
    label: str = Field(..., description="Display label for the node")
    properties: Properties = Field(..., description="Node properties")

class Edge(BaseModel):
    id: str = Field(..., description="Unique identifier for the edge")
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    type: str = Field(..., description="Edge type (transition, triggers, sends)")
    label: str = Field(..., description="Display label for the edge")
class RegistrationProcedure(BaseModel):
    procedure_name: str = Field(..., description="Name of the procedure (Initial Registration or Periodic Registration Update)")
    nodes: List[Node] = Field(..., description="Graph nodes")
    edges: List[Edge] = Field(..., description="Graph edges")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional procedure metadata")

class RegistrationProcedures(BaseModel):
    procedures: List[RegistrationProcedure] = Field(..., description="List of registration procedures")

    def __init__(self, **data):
        # Ensure we have both procedure types
        if 'procedures' in data:
            proc_names = {p['procedure_name'] for p in data['procedures']}
            if 'Initial Registration' not in proc_names:
                data['procedures'].append({
                    'procedure_name': 'Initial Registration',
                    'nodes': [], 'edges': []
                })
            if 'Periodic Registration Update' not in proc_names:
                data['procedures'].append({
                    'procedure_name': 'Periodic Registration Update',
                    'nodes': [], 'edges': []
                })
        super().__init__(**data)

class PropertyGraph(BaseModel):
    procedure_name: str = Field(..., description="Name of the procedure")
    procedure_type: str = Field(..., description="Type of procedure")
    nodes: List[Node] = Field(..., description="Graph nodes")
    edges: List[Edge] = Field(..., description="Graph edges")

    @classmethod
    def from_dict(cls, data: Dict) -> 'PropertyGraph':
        """Create PropertyGraph from raw dictionary, handling missing fields"""
        # Ensure required fields exist
        if 'procedure_name' not in data:
            raise ValueError("procedure_name is required")
            
        # Set procedure_type from name if not provided
        if 'procedure_type' not in data:
            data['procedure_type'] = data['procedure_name']
            
        # Initialize empty lists if not provided
        if 'nodes' not in data:
            data['nodes'] = []
        if 'edges' not in data:
            data['edges'] = []
            
        return cls(**data)

class ExtractionResponse(BaseModel):
    procedures: List[PropertyGraph]

    @classmethod
    def from_dict(cls, data: Dict) -> 'ExtractionResponse':
        """Create ExtractionResponse from raw dictionary"""
        if isinstance(data, dict):
            # If single procedure
            if 'procedure_name' in data:
                return cls(procedures=[PropertyGraph.from_dict(data)])
            # If list of procedures in different format
            if 'procedures' in data:
                return cls(procedures=[PropertyGraph.from_dict(p) for p in data['procedures']])
            
        # If list of procedures directly
        if isinstance(data, list):
            return cls(procedures=[PropertyGraph.from_dict(p) for p in data])
            
        raise ValueError("Invalid data format")

class ProcedureExtractor:
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize Gemini API and configure the model"""
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model_name)
        self.generation_config = {
            "temperature": 0,
            "top_p": 0.8,
            "top_k": 40,
            # "max_output_tokens": 8000
        }

    def _create_query_based_prompt(self, query: str, chunks: List[Dict], doc_title: str) -> str:
        chunks_text = "\n\n".join([
            f"Section {chunk['title']}\nContent: {chunk['content']}"
            for chunk in chunks
        ])
        
        return f"""You are a 3GPP specification expert. Extract mentioned procedures as property graphs.

        For EACH procedure mentioned in the query:
        {query}

        Context:
        {chunks_text}

        Return procedures in this exact JSON schema:
        {json.dumps(RegistrationProcedures.model_json_schema(), indent=2)}

        Ensure:
        1. Each node has a unique ID
        2. Edges connect nodes using their IDs
        3. All properties include section references
        4. Message flows are properly captured
        """

    def _parse_response(self, response_text: str, doc_title: str) -> List[Dict]:
        try:
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]

            data = json.loads(cleaned_text.strip())
            
            # Use the new from_dict methods to handle various response formats
            try:
                validated_data = ExtractionResponse.from_dict(data)
                return [proc.dict() for proc in validated_data.procedures]
            except ValidationError as e:
                print(f"First validation attempt failed: {e}")
                # Try wrapping in procedures list if single procedure
                if isinstance(data, dict) and 'procedure_name' in data:
                    validated_data = ExtractionResponse(procedures=[PropertyGraph.from_dict(data)])
                    return [proc.dict() for proc in validated_data.procedures]
                raise
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text[:200]}...")
            return []
        except ValidationError as e:
            print(f"Validation error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def extract_procedures_from_query(self, query: str, relevant_chunks: List[Dict], doc_title: str) -> List[Dict]:
        """Extract property graph representation of procedures"""
        prompt = self._create_query_based_prompt(query, relevant_chunks, doc_title)
        
        try:
            response = self.client.generate_content(
                contents=prompt,
                generation_config=self.generation_config
            )
            
            if response.text:
                return self._parse_response(response.text, doc_title)
            return []
            
        except Exception as e:
            print(f"Error extracting procedures: {e}")
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

