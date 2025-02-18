class MermaidGenerator:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def generate_attach_procedure_diagram(self) -> str:
        """Generate a Mermaid diagram specifically for the attach procedure"""
        mermaid_code = [
            "graph TB",
            "    %% Styling",
            "    classDef state fill:#f9f,stroke:#333,stroke-width:2px;",
            "    classDef action fill:#bbf,stroke:#333,stroke-width:1px;",
            "    classDef parameter fill:#bfb,stroke:#333,stroke-width:1px;",
            "    classDef event fill:#fbf,stroke:#333,stroke-width:1px;",
            "    classDef conditional fill:#ffd,stroke:#333,stroke-width:1px;",
            "    %% Node definitions"
        ]
        
        processed_nodes = set()
        processed_edges = set()
        
        with self.driver.session() as session:
            # First check if we have any nodes
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()["count"]
            
            if count == 0:
                # If database is empty, create a basic attach procedure diagram
                mermaid_code.extend([
                    "    %% Initial State",
                    "    EMM_DEREGISTERED[EMM-DEREGISTERED]:::state",
                    "    %% Actions",
                    "    ATTACH_REQUEST[UE: Send Attach Request]:::action",
                    "    AUTHENTICATION[MME: Authenticate UE]:::action",
                    "    SECURITY_MODE[MME: Security Mode Command]:::action",
                    "    ATTACH_ACCEPT[MME: Send Attach Accept]:::action",
                    "    ATTACH_COMPLETE[UE: Send Attach Complete]:::action",
                    "    %% Final State",
                    "    EMM_REGISTERED[EMM-REGISTERED]:::state",
                    "    %% Parameters",
                    "    IMSI[IMSI/GUTI]:::parameter",
                    "    AUTH_PARAMS[Authentication Parameters]:::parameter",
                    "    SEC_PARAMS[Security Parameters]:::parameter",
                    "    BEARER_PARAMS[Bearer Parameters]:::parameter",
                    "    %% Flow",
                    "    EMM_DEREGISTERED -->|1| ATTACH_REQUEST",
                    "    ATTACH_REQUEST -->|2| AUTHENTICATION",
                    "    AUTHENTICATION -->|3| SECURITY_MODE",
                    "    SECURITY_MODE -->|4| ATTACH_ACCEPT",
                    "    ATTACH_ACCEPT -->|5| ATTACH_COMPLETE",
                    "    ATTACH_COMPLETE -->|6| EMM_REGISTERED",
                    "    %% Parameter Usage",
                    "    ATTACH_REQUEST -.->|uses| IMSI",
                    "    AUTHENTICATION -.->|uses| AUTH_PARAMS",
                    "    SECURITY_MODE -.->|uses| SEC_PARAMS",
                    "    ATTACH_ACCEPT -.->|uses| BEARER_PARAMS"
                ])
            else:
                # Query for attach procedure elements with proper relationships
                result = session.run("""
                MATCH (n)
                WHERE (n:State OR n:Action OR n:Event OR n:Parameter)
                AND (n.name CONTAINS 'ATTACH' OR n.name CONTAINS 'EMM' OR n.type = 'EMM')
                OPTIONAL MATCH (n)-[r]->(m)
                WHERE type(r) IN ['TRANSITIONS_TO', 'TRIGGERS', 'USES_PARAMETER', 'LEADS_TO']
                RETURN n, r, m, labels(n) as node_labels
                ORDER BY 
                    CASE 
                        WHEN 'State' IN labels(n) THEN 1
                        WHEN 'Action' IN labels(n) THEN 2
                        WHEN 'Event' IN labels(n) THEN 3
                        WHEN 'Parameter' IN labels(n) THEN 4
                        ELSE 5
                    END
                """)
                
                for record in result:
                    source_node = record["n"]
                    rel = record["r"]
                    target_node = record["m"]
                    node_labels = record["node_labels"]
                    
                    # Process source node
                    if source_node and source_node["name"] not in processed_nodes:
                        node_id = source_node["name"].replace(" ", "_")
                        node_label = f"{source_node['name']}"
                        if source_node.get("actor"):
                            node_label = f"{source_node['actor']}: {node_label}"
                        
                        # Add node with proper styling
                        if "State" in node_labels:
                            mermaid_code.append(f"    {node_id}[{node_label}]:::state")
                        elif "Action" in node_labels:
                            mermaid_code.append(f"    {node_id}[{node_label}]:::action")
                        elif "Parameter" in node_labels:
                            mermaid_code.append(f"    {node_id}[{node_label}]:::parameter")
                        elif "Event" in node_labels:
                            mermaid_code.append(f"    {node_id}[{node_label}]:::event")
                        
                        processed_nodes.add(source_node["name"])
                    
                    # Process relationship and target node
                    if rel and target_node:
                        source_id = source_node["name"].replace(" ", "_")
                        target_id = target_node["name"].replace(" ", "_")
                        edge_key = f"{source_id}-{target_id}"
                        
                if edge_key not in processed_edges:
                            # Add target node if not already added
                            if target_node["name"] not in processed_nodes:
                                node_label = f"{target_node['name']}"
                                if target_node.get("actor"):
                                    node_label = f"{target_node['actor']}: {node_label}"
                                
                                if "State" in str(target_node.labels):
                                    mermaid_code.append(f"    {target_id}[{node_label}]:::state")
                                elif "Action" in str(target_node.labels):
                                    mermaid_code.append(f"    {target_id}[{node_label}]:::action")
                                elif "Parameter" in str(target_node.labels):
                                    mermaid_code.append(f"    {target_id}[{node_label}]:::parameter")
                                elif "Event" in str(target_node.labels):
                                    mermaid_code.append(f"    {target_id}[{node_label}]:::event")
                                
                                processed_nodes.add(target_node["name"])
                            
                            # Add relationship with proper styling
                            rel_type = rel.type
                            if rel_type == "TRANSITIONS_TO":
                                sequence = rel.get("sequence", "")
                                mermaid_code.append(f"    {source_id} -->|{sequence}| {target_id}")
                            elif rel_type == "USES_PARAMETER":
                                mermaid_code.append(f"    {source_id} -.->|uses| {target_id}")
                            elif rel_type == "TRIGGERS":
                                mermaid_code.append(f"    {source_id} ==>|triggers| {target_id}")
                            elif rel_type == "LEADS_TO":
                                conditions = rel.get("conditions", [])
                                if conditions:
                                    mermaid_code.append(f"    {source_id} -->|{', '.join(conditions)}| {target_id}")
                                else:
                                    mermaid_code.append(f"    {source_id} --> {target_id}")
                            
                            processed_edges.add(edge_key)
        
        return "\n".join(mermaid_code) 