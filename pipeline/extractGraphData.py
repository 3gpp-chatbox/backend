'''
Use LLM to dynamically extract and structure graph data from procedure JSON.
The LLM will analyze the procedures and create a graph representation
'''

import google.generativeai as genai
from typing import List, Dict, Any
import json
from pydantic import BaseModel, Field
import os
import sys

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

def extract_nodes_and_edges(procedures: List[Dict[str, Any]], api_key: str) -> Dict[str, Dict[str, Any]]:
    """Extract graph data for each procedure separately"""
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Store graph data for each procedure
    procedure_graphs = {}
    
    for procedure in procedures:
        procedure_name = procedure.get('procedure_name', 'Unknown')
        print(f"\nExtracting graph for procedure: {procedure_name}")
        
        # Create prompt for this specific procedure
        prompt = f"""You are a graph structure expert. Create a graph representation of this 5G NAS procedure.

Input Procedure:
{json.dumps(procedure, indent=2)}

Task: Convert the procedure into a graph with nodes and edges.

Instructions:
1. Create nodes for each:
   - State from States list
   - Trigger from Triggers list
   - Action from Actions list
   - Message from Message_Types

2. Create edges to show:
   - State transitions (following Flow_of_execution)
   - Message flows
   - Trigger-to-state connections
   - Action sequences

3. Add relevant properties from:
   - Error_Handling
   - Expected_Outcomes
   - References
   - Causes

Return ONLY a valid JSON object following this schema (no other text):
{json.dumps(GraphData.model_json_schema(), indent=2)}"""

        try:
            # Get LLM response
            response = model.generate_content(prompt)
            
            if not response.text:
                print(f"✗ Empty response for {procedure_name}")
                continue
            
            # Clean the response text
            cleaned_text = response.text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
                
            # Parse and validate response
            print(f"Parsing response for {procedure_name}...")
            graph_data = json.loads(cleaned_text)
            validated_data = GraphData(**graph_data)
            
            # Add procedure metadata
            graph_data = validated_data.model_dump()
            graph_data['metadata'].update({
                'procedure_name': procedure_name,
                'category': procedure.get('procedure_category', 'Unknown'),
                'total_nodes': len(graph_data['nodes']),
                'total_edges': len(graph_data['edges'])
            })
            
            # Store graph data for this procedure
            procedure_graphs[procedure_name] = graph_data
            print(f"✓ Generated graph with {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges")
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error for {procedure_name}: {e}")
            print(f"Response text: {response.text[:200]}...")
        except Exception as e:
            print(f"✗ Error processing {procedure_name}: {e}")
    
    return procedure_graphs

# def store_in_neo4j(graph_data: Dict[str, Any], neo4j_uri: str, neo4j_user: str, neo4j_password: str):
#     """Store the graph data in Neo4j with a structured model"""
#     from neo4j import GraphDatabase

#     driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

#     def create_graph(tx, data):
#         procedure_name = data['metadata'].get('procedure_name', 'Unknown')

#         # Clear existing data for this procedure
#         tx.run("MATCH (n {procedure: $procedure}) DETACH DELETE n", procedure=procedure_name)

#         node_mapping = {}  # Store node IDs for creating relationships

#         # Create main nodes (States, Triggers, Actions, Messages)
#         for node in data['nodes']:
#             node_id = node['id']
#             node_mapping[node_id] = node 

#             tx.run("""
#                 CREATE (n:ProcedureNode {
#                     id: $id,
#                     label: $label,
#                     type: $type,
#                     procedure: $procedure
#                 })
#             """, {
#                 'id': node_id,
#                 'label': node['label'],
#                 'type': node['type'],
#                 'procedure': procedure_name
#             })

#             # Handle complex properties as separate nodes
#             for key, value in node.get('properties', {}).items():
#                 if isinstance(value, (dict, list)):  # If complex, create separate node
#                     prop_id = f"{node_id}_{key}"
#                     tx.run("""
#                         CREATE (p:PropertyNode {
#                             id: $prop_id,
#                             key: $key,
#                             value: $value
#                         })
#                     """, {
#                         'prop_id': prop_id,
#                         'key': key,
#                         'value': json.dumps(value) 
#                     })

#                     tx.run("""
#                         MATCH (n:ProcedureNode {id: $node_id})
#                         MATCH (p:PropertyNode {id: $prop_id})
#                         CREATE (n)-[:HAS_PROPERTY]->(p)
#                     """, {
#                         'node_id': node_id,
#                         'prop_id': prop_id
#                     })

#         # Create relationships (Transitions, Triggers, etc.)
#         for edge in data['edges']:
#             source_id = edge['source']
#             target_id = edge['target']
#             tx.run("""
#                 MATCH (source:ProcedureNode {id: $source})
#                 MATCH (target:ProcedureNode {id: $target})
#                 CREATE (source)-[:TRANSITION {id: $id, label: $label, type: $type}]->(target)
#             """, {
#                 'source': source_id,
#                 'target': target_id,
#                 'id': edge['id'],
#                 'label': edge['label'],
#                 'type': edge['type']
#             })

#     with driver.session() as session:
#         session.execute_write(create_graph, graph_data)
#         print("✓ Successfully stored graph in Neo4j")

#     driver.close()

# def get_neo4j_graph(neo4j_uri: str, neo4j_user: str, neo4j_password: str, procedure_name: str) -> Dict[str, Any]:
#     """Retrieve graph data from Neo4j for a specific procedure"""
#     try:
#         from neo4j import GraphDatabase
        
#         driver = GraphDatabase.driver(
#             neo4j_uri, 
#             auth=(neo4j_user, neo4j_password)
#         )

#         def fetch_graph(tx, procedure):
#             # Get nodes
#             nodes_result = tx.run("""
#                 MATCH (n:ProcedureNode {procedure: $procedure})
#                 RETURN collect({
#                     id: n.id,
#                     label: n.label,
#                     type: n.type,
#                     properties: n.properties
#                 }) as nodes
#             """, procedure=procedure)
            
#             # Get relationships
#             edges_result = tx.run("""
#                 MATCH (source:ProcedureNode {procedure: $procedure})-[r:TRANSITION]->(target:ProcedureNode {procedure: $procedure})
#                 RETURN collect({
#                     id: r.id,
#                     source: source.id,
#                     target: target.id,
#                     label: r.label,
#                     type: r.type,
#                     properties: r.properties
#                 }) as edges
#             """, procedure=procedure)
            
#             nodes = nodes_result.single()['nodes']
#             edges = edges_result.single()['edges']
            
#             return {
#                 'nodes': nodes,
#                 'edges': edges,
#                 'metadata': {'procedure_name': procedure}
#             }

#         with driver.session() as session:
#             return session.execute_read(fetch_graph, procedure_name)
            
#     except Exception as e:
#         print(f"Error retrieving from Neo4j: {e}")
#         return {'nodes': [], 'edges': [], 'metadata': {}}
#     finally:
#         if 'driver' in locals():
#             driver.close()

# For testing
# if __name__ == "__main__":
#     try:
#         # Read the registration procedures file
#         file_path = "../output/8_registration_procedures.json"
#         if not os.path.exists(file_path):
#             print(f"Error: File not found: {file_path}")
#             sys.exit(1)
            
#         with open(file_path, "r") as f:
#             procedures = json.load(f)
        
#         if not procedures:
#             print("Error: No procedures found in input file")
#             sys.exit(1)
            
#         # Get API key
#         sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#         from config import Gemini_API_KEY
        
#         if not Gemini_API_KEY:
#             print("Error: No API key found")
#             sys.exit(1)
        
#         # Extract graph data
#         print("\nExtracting graph data...")
#         graph_data = extract_nodes_and_edges(procedures, Gemini_API_KEY)
        
#         if not graph_data["nodes"]:
#             print("Warning: No nodes generated in graph data")
        
#         # Save to file
#         output_dir = "../graphs"
#         os.makedirs(output_dir, exist_ok=True)
        
#         output_path = os.path.join(output_dir, "registration_graph.json")
#         with open(output_path, "w") as f:
#             json.dump(graph_data, f, indent=2)
        
#         print(f"\n✓ Graph data saved to {output_path}")
#         print(f"  - Nodes: {len(graph_data['nodes'])}")
#         print(f"  - Edges: {len(graph_data['edges'])}")
        
#     except Exception as e:
#         print(f"\nError in main: {e}")
#         sys.exit(1)
