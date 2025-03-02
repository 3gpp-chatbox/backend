'''
Use LLM to dynamically extract and structure graph data from procedure JSON.
The LLM will analyze the procedures and create a graph representation
that can be stored in Neo4j and visualized in React.
'''

import google.generativeai as genai
from typing import List, Dict, Any
import json
from pydantic import BaseModel, Field
import os

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    metadata: Dict[str, Any] = Field(default_factory=dict)

def extract_nodes_and_edges(procedures: List[Dict[str, Any]], api_key: str) -> Dict[str, Any]:
    """Use LLM to extract graph structure from procedures"""
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Create prompt with procedure data and desired structure
    prompt = f"""
    Analyze these 5G NAS procedures and create a graph representation.
    
    Input Procedures:
    {json.dumps(procedures, indent=2)}
    
    Instructions:
    1. Extract nodes representing:
       - States (e.g., "REGISTERED", "DEREGISTERED")
       - Events/Triggers (e.g., "Registration Request", "Authentication")
       
    2. Create edges representing:
       - Actions (transitions between states)
       - Message flows (between entities)
       
    3. Add properties including:
       - Message types
       - References to 3GPP specs
       - Timing constraints
       - Success/failure conditions
    
    Output the graph data in this JSON structure:
    {GraphData.model_json_schema_str()}
    
    Ensure:
    - Unique IDs for nodes and edges
    - Clear labels describing each element
    - Proper source/target connections
    - Relevant properties and metadata
    """
    
    try:
        # Get LLM response
        response = model.generate_content(prompt)
        
        if not response.text:
            raise ValueError("Empty response from LLM")
            
        # Parse and validate response
        graph_data = json.loads(response.text)
        validated_data = GraphData(**graph_data)
        
        return validated_data.model_dump()
        
    except Exception as e:
        print(f"Error extracting graph data: {e}")
        # Return empty graph structure if extraction fails
        return GraphData(nodes=[], edges=[], metadata={}).model_dump()

def store_in_neo4j(graph_data: Dict[str, Any], neo4j_uri: str, neo4j_user: str, neo4j_password: str):
    """Store the graph data in Neo4j database"""
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            neo4j_uri, 
            auth=(neo4j_user, neo4j_password)
        )
        
        def create_graph(tx, data):
            # Clear existing data
            tx.run("MATCH (n) DETACH DELETE n")
            
            # Create nodes
            for node in data['nodes']:
                tx.run("""
                    CREATE (n:Node {
                        id: $id,
                        label: $label,
                        type: $type,
                        properties: $properties
                    })
                """, node)
            
            # Create edges
            for edge in data['edges']:
                tx.run("""
                    MATCH (source:Node {id: $source})
                    MATCH (target:Node {id: $target})
                    CREATE (source)-[r:TRANSITION {
                        id: $id,
                        label: $label,
                        type: $type,
                        properties: $properties
                    }]->(target)
                """, edge)
        
        with driver.session() as session:
            session.execute_write(create_graph, graph_data)
            
        print("✓ Successfully stored graph in Neo4j")
        
    except Exception as e:
        print(f"Error storing in Neo4j: {e}")
    finally:
        if 'driver' in locals():
            driver.close()
