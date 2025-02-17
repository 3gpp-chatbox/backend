from neo4j import GraphDatabase
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jToMermaid:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def generate_state_machine_diagram(self, protocol_type: str = None) -> str:
        """Generate a Mermaid state diagram for a specific protocol type"""
        query = """
        MATCH (s1:State)-[r:TRANSITIONS_TO]->(s2:State)
        WHERE s1.type = $protocol_type
        RETURN s1.name as from_state, s2.name as to_state, 
               r.conditions as conditions, r.confidence as confidence
        ORDER BY r.confidence DESC
        """
        
        mermaid_lines = ["stateDiagram-v2"]
        
        with self.driver.session() as session:
            result = session.run(query, protocol_type=protocol_type)
            for record in result:
                from_state = record["from_state"].replace(" ", "_")
                to_state = record["to_state"].replace(" ", "_")
                conditions = record["conditions"]
                confidence = record["confidence"]
                
                # Add transition with conditions if they exist
                if conditions:
                    condition_text = " & ".join(conditions[:2])  # Limit to first 2 conditions for clarity
                    mermaid_lines.append(f"    {from_state} --> {to_state}: {condition_text}")
                else:
                    mermaid_lines.append(f"    {from_state} --> {to_state}")
        
        return "\n".join(mermaid_lines)

    def generate_procedure_flow(self, procedure_name: str) -> str:
        """Generate a Mermaid flow diagram for a specific procedure"""
        query = """
        MATCH path = (start:Action)-[r:TRIGGERS|IMPACTS*1..5]->(end:State)
        WHERE start.name CONTAINS $procedure_name
        RETURN path
        LIMIT 15
        """
        
        mermaid_lines = ["graph TD"]
        processed_relationships = set()
        
        with self.driver.session() as session:
            result = session.run(query, procedure_name=procedure_name)
            for record in result:
                path = record["path"]
                nodes = path.nodes
                rels = path.relationships
                
                for rel in rels:
                    rel_key = f"{rel.start_node['name']}-{rel.type}-{rel.end_node['name']}"
                    if rel_key not in processed_relationships:
                        start_node = rel.start_node["name"].replace(" ", "_")
                        end_node = rel.end_node["name"].replace(" ", "_")
                        
                        # Add nodes with different shapes based on type
                        if "Action" in rel.start_node.labels:
                            mermaid_lines.append(f"    {start_node}[{rel.start_node['name']}]")
                        elif "Event" in rel.start_node.labels:
                            mermaid_lines.append(f"    {start_node}({rel.start_node['name']})")
                        elif "State" in rel.start_node.labels:
                            mermaid_lines.append(f"    {start_node}{{{rel.start_node['name']}}}")
                        
                        # Add relationship
                        if rel.type == "TRIGGERS":
                            mermaid_lines.append(f"    {start_node} -->|triggers| {end_node}")
                        elif rel.type == "IMPACTS":
                            mermaid_lines.append(f"    {start_node} -.->|impacts| {end_node}")
                        else:
                            mermaid_lines.append(f"    {start_node} --> {end_node}")
                        
                        processed_relationships.add(rel_key)
        
        return "\n".join(mermaid_lines)

    def generate_parameter_dependencies(self, procedure_name: str = None) -> str:
        """Generate a Mermaid diagram showing parameter dependencies"""
        query = """
        MATCH (p1:Parameter)-[r:DEPENDS_ON]->(p2:Parameter)
        WHERE p1.mandatory = true
        RETURN p1.name as param1, p2.name as param2, p1.type as type1, p2.type as type2
        """
        
        mermaid_lines = ["graph LR"]
        processed_params = set()
        
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                param1 = record["param1"].replace(" ", "_")
                param2 = record["param2"].replace(" ", "_")
                type1 = record["type1"]
                type2 = record["type2"]
                
                # Add nodes with type information
                if param1 not in processed_params:
                    mermaid_lines.append(f"    {param1}[{record['param1']}<br/>{type1}]")
                    processed_params.add(param1)
                if param2 not in processed_params:
                    mermaid_lines.append(f"    {param2}[{record['param2']}<br/>{type2}]")
                    processed_params.add(param2)
                
                # Add dependency relationship
                mermaid_lines.append(f"    {param1} -->|depends on| {param2}")
        
        return "\n".join(mermaid_lines)

    def generate_event_chain(self, max_depth: int = 3) -> str:
        """Generate a Mermaid diagram showing event chains"""
        query = """
        MATCH path = (e1:Event)-[r*1..3]->(e2:Event)
        RETURN path
        LIMIT 10
        """
        
        mermaid_lines = ["graph LR"]
        processed_events = set()
        
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                path = record["path"]
                nodes = path.nodes
                rels = path.relationships
                
                for i, node in enumerate(nodes):
                    node_id = node["name"].replace(" ", "_")
                    if node_id not in processed_events:
                        mermaid_lines.append(f"    {node_id}({node['name']})")
                        processed_events.add(node_id)
                
                for rel in rels:
                    start_node = rel.start_node["name"].replace(" ", "_")
                    end_node = rel.end_node["name"].replace(" ", "_")
                    mermaid_lines.append(f"    {start_node} -->|leads to| {end_node}")
        
        return "\n".join(mermaid_lines)

    def export_diagram(self, mermaid_code: str, output_file: str):
        """Export the Mermaid diagram to a markdown file"""
        with open(output_file, "w") as f:
            f.write("# 3GPP Protocol Diagram\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_code)
            f.write("\n```")

def main():
    converter = Neo4jToMermaid()
    
    # Generate and export state machine diagram
    state_diagram = converter.generate_state_machine_diagram(protocol_type="5GMM")
    converter.export_diagram(state_diagram, "5gmm_state_machine.md")
    
    # Generate and export procedure flow
    procedure_diagram = converter.generate_procedure_flow("Registration")
    converter.export_diagram(procedure_diagram, "registration_procedure.md")
    
    # Generate and export parameter dependencies
    param_diagram = converter.generate_parameter_dependencies()
    converter.export_diagram(param_diagram, "parameter_dependencies.md")
    
    # Generate and export event chain
    event_diagram = converter.generate_event_chain()
    converter.export_diagram(event_diagram, "event_chain.md")
    
    converter.close()

if __name__ == "__main__":
    main() 