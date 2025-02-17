from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables
load_dotenv()

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

console = Console()

class MermaidGenerator:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def generate_state_diagram(self, limit: int = 50) -> str:
        """Generate a state diagram showing state transitions"""
        mermaid_code = ["stateDiagram-v2"]
        
        with self.driver.session() as session:
            # Get states and their transitions with conditions
            result = session.run("""
            MATCH (s1:State)-[r:TRANSITIONS_TO|IMPACTS|TRIGGERS]->(s2:State)
            WHERE s1.type = s2.type  // Only show transitions between same type states
            RETURN DISTINCT s1.name as source, s2.name as target, 
                   s1.type as type, s1.section as section,
                   collect(DISTINCT r.description) as descriptions
            ORDER BY s1.type, s1.section
            LIMIT $limit
            """, limit=limit)
            
            # Group states by type
            for record in result:
                source = record["source"].replace(" ", "_")
                target = record["target"].replace(" ", "_")
                state_type = record["type"]
                section = record["section"]
                descriptions = record["descriptions"]
                
                # Add state transition with type and section info
                if descriptions and descriptions[0]:
                    desc = descriptions[0][:50] + "..." if len(descriptions[0]) > 50 else descriptions[0]
                    mermaid_code.append(f"    {source} --> {target}: {desc}")
                else:
                    mermaid_code.append(f"    {source} --> {target}")
                
                # Add notes for important states
                if section:
                    mermaid_code.append(f"    note right of {source}: {state_type}<br/>Section: {section}")
        
        return "\n".join(mermaid_code)

    def generate_procedure_flow(self, procedure_name: str = "Registration") -> str:
        """Generate a flow diagram for a specific procedure"""
        mermaid_code = [
            "graph TB",
            "    %% Node styling",
            "    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;",
            "    classDef ue fill:#d4e6ff,stroke:#0066cc,stroke-width:2px;",
            "    classDef amf fill:#ffe6cc,stroke:#ff9933,stroke-width:2px;",
            "    classDef param fill:#e6ffe6,stroke:#33cc33,stroke-width:1px;",
            "    linkStyle default stroke:#666,stroke-width:1px;"
        ]
        
        with self.driver.session() as session:
            # Get all actions in sequence
            result = session.run("""
            MATCH (a:Action)
            RETURN a.name as name, a.actor as actor, a.description as description, 
                   a.step_number as step
            ORDER BY a.step_number
            """)
            
            # Process actions and their parameters
            for record in result:
                step = record["step"]
                name = record["name"].replace(" ", "_")
                actor = record["actor"]
                desc = record["description"]
                
                # Format node with step number and description
                node_text = f"Step {step}: {record['name']}<br/>{desc}"
                
                # Style node based on actor
                if actor == "UE":
                    mermaid_code.append(f"    {name}[{node_text}]:::ue")
                else:
                    mermaid_code.append(f"    {name}[{node_text}]:::amf")
                
                # Get parameters for this action
                param_result = session.run("""
                MATCH (a:Action {name: $name})-[:USES_PARAMETER]->(p:Parameter)
                RETURN p.name as param
                """, name=record["name"])
                
                # Add parameter nodes
                for param_record in param_result:
                    param_name = param_record["param"].replace(" ", "_")
                    mermaid_code.append(f"    {param_name}[{param_record['param']}]:::param")
                    mermaid_code.append(f"    {name} -.->|uses| {param_name}")
                
                # Add relationship to next step
                if step < 6:  # Not the last step
                    next_result = session.run("""
                    MATCH (a:Action {step_number: $next_step})
                    RETURN a.name as next_name
                    """, next_step=step + 1)
                    
                    if next_result.peek():
                        next_name = next_result.single()["next_name"].replace(" ", "_")
                        mermaid_code.append(f"    {name} -->|triggers| {next_name}")
        
        return "\n".join(mermaid_code)

    def generate_parameter_dependencies(self) -> str:
        """Generate a diagram showing parameter dependencies"""
        mermaid_code = ["""graph TB
        %% Configure graph layout
        classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
        classDef category fill:#e1e1e1,stroke:#666,stroke-width:2px;
        linkStyle default stroke:#666,stroke-width:1px;
        """]
        
        processed_nodes = set()
        processed_edges = set()
        
        with self.driver.session() as session:
            # Get parameter dependencies with improved categorization
            result = session.run("""
            MATCH (p1:Parameter)-[r:DEPENDS_ON|USES_PARAMETER]->(p2:Parameter)
            WHERE p1 <> p2  // Exclude self-references
            WITH p1, p2, r,
                 CASE 
                    WHEN p1.type IS NOT NULL THEN p1.type
                    WHEN p1.name =~ '(?i).*(TAI|PLMN|TAC|cell|area).*' THEN 'Location'
                    WHEN p1.name =~ '(?i).*(security|KSI|eKSI|key|auth).*' THEN 'Security'
                    WHEN p1.name =~ '(?i).*(bearer|PDU|QoS).*' THEN 'Bearer'
                    WHEN p1.name =~ '(?i).*(message|container|IE|payload).*' THEN 'Message'
                    WHEN p1.name =~ '(?i).*(IMSI|GUTI|identity).*' THEN 'Identity'
                    WHEN p1.name =~ '(?i).*(timer|counter|retry).*' THEN 'Timer'
                    ELSE 'Other'
                 END as category,
                 CASE TYPE(r)
                    WHEN 'DEPENDS_ON' THEN 'requires'
                    WHEN 'USES_PARAMETER' THEN 'uses'
                    ELSE 'depends on'
                 END as rel_type
            RETURN p1.name as param1, p2.name as param2,
                   category,
                   p1.description as desc1, p2.description as desc2,
                   rel_type
            ORDER BY category, param1
            LIMIT 40
            """)
            
            current_category = None
            for record in result:
                param1 = record["param1"].replace(" ", "_")
                param2 = record["param2"].replace(" ", "_")
                category = record["category"]
                rel_type = record["rel_type"]
                
                # Format descriptions - take first sentence and clean it
                desc1 = record["desc1"]
                if desc1:
                    desc1 = desc1.split('.')[0].strip()
                    if len(desc1) > 50:
                        desc1 = desc1[:47] + "..."
                
                desc2 = record["desc2"]
                if desc2:
                    desc2 = desc2.split('.')[0].strip()
                    if len(desc2) > 50:
                        desc2 = desc2[:47] + "..."
                
                # Add subgraph for each category with styling
                if category != current_category:
                    if current_category:
                        mermaid_code.append("    end")
                    mermaid_code.append(f"""    subgraph {category}
    style {category} fill:#e1e1e1,stroke:#666,stroke-width:2px""")
                    current_category = category
                
                # Add nodes with descriptions if not already added
                if param1 not in processed_nodes:
                    node_text = record["param1"]
                    if desc1:
                        node_text += f"<br/>{desc1}"
                    mermaid_code.append(f"    {param1}[{node_text}]")
                    processed_nodes.add(param1)
                
                if param2 not in processed_nodes:
                    node_text = record["param2"]
                    if desc2:
                        node_text += f"<br/>{desc2}"
                    mermaid_code.append(f"    {param2}[{node_text}]")
                    processed_nodes.add(param2)
                
                # Add relationship if not already added
                edge_key = f"{param1}-{param2}"
                if edge_key not in processed_edges:
                    mermaid_code.append(f"    {param1} -->|{rel_type}| {param2}")
                    processed_edges.add(edge_key)
            
            if current_category:
                mermaid_code.append("    end")
        
        return "\n".join(mermaid_code)

    def export_diagrams(self, output_dir: str = "diagrams"):
        """Export all diagram types to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate and save state diagram
        state_diagram = self.generate_state_diagram()
        with open(os.path.join(output_dir, "state_diagram.md"), "w") as f:
            f.write("# 3GPP Protocol State Diagram\n\n")
            f.write("```mermaid\n")
            f.write(state_diagram)
            f.write("\n```")
        
        # Generate and save procedure flow
        procedure_flow = self.generate_procedure_flow("Registration")
        with open(os.path.join(output_dir, "procedure_flow.md"), "w") as f:
            f.write("# 5G Registration Procedure Flow\n\n")
            f.write("```mermaid\n")
            f.write(procedure_flow)
            f.write("\n```")
        
        # Generate and save parameter dependencies
        param_diagram = self.generate_parameter_dependencies()
        with open(os.path.join(output_dir, "parameter_dependencies.md"), "w") as f:
            f.write("# 5G Registration Parameter Dependencies\n\n")
            f.write("```mermaid\n")
            f.write(param_diagram)
            f.write("\n```")
        
        console.print(f"[green]Diagrams exported to {output_dir}/[/green]")

if __name__ == "__main__":
    try:
        console.print("[bold blue]Generating Mermaid diagrams from Neo4j...[/bold blue]")
        generator = MermaidGenerator()
        generator.export_diagrams()
        generator.close()
        console.print("[bold green]✅ Successfully generated all diagrams![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]") 