import networkx as nx
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import json
import os

# Use os.path.join for cross-platform compatibility
file_path = os.path.join("processed_data", "intermediate_results_batch_4_of_76.json")
extracted_data = json.load(open(file_path))

def create_plotly_graph(data):
    G = nx.DiGraph()
    node_types = {}

    for result in data["results"]:  # Iterate over all result entries
        # Add states first
        for state in result.get("states", []):
            G.add_node(state["name"], 
                      node_type="state",
                      type=state["type"], 
                      label=state["name"],
                      description=state.get("description", ""))
            node_types[state["name"]] = "state"

        # Add network elements
        for element in result.get("network_elements", []):
            G.add_node(element["name"], 
                      node_type="network_element",
                      type=element["type"], 
                      label=element["name"],
                      description=element.get("description", ""))
            node_types[element["name"]] = "network_element"

        # Add network element relationships with orange color
        for relation in result.get("network_element_relationships", []):
            G.add_edge(relation["element1"], 
                      relation["element2"], 
                      edge_type="relationship",
                      relationship=relation["relationship"],
                      color='rgba(255, 165, 0, 0.6)',  # Orange with transparency
                      description=f"Network Relationship\n{relation['relationship']}")

        # Add edges for transitions with blue color and connect network elements to states
        for transition in result.get("transitions", []):
            from_state = transition["from_state"]
            to_state = transition["to_state"]
            
            # Add the state transition
            G.add_edge(from_state, 
                      to_state, 
                      edge_type="transition",
                      trigger=transition.get("trigger", ""),
                      condition=transition.get("condition", ""),
                      color='rgba(0, 0, 255, 0.6)',  # Blue with transparency
                      description=f"State Transition\nTrigger: {transition.get('trigger', 'N/A')}\nCondition: {transition.get('condition', 'N/A')}")
            
            # Find network elements involved in this transition
            trigger = transition.get("trigger", "").lower()
            for element in G.nodes():
                if node_types.get(element) == "network_element":
                    element_name = element.lower()
                    # If the network element is mentioned in the trigger or states
                    if (element_name in trigger or 
                        element_name in from_state.lower() or 
                        element_name in to_state.lower()):
                        # Connect network element to both states with green edges
                        G.add_edge(element, 
                                 from_state,
                                 edge_type="element_state",
                                 color='rgba(0, 255, 0, 0.6)',  # Green with transparency
                                 description=f"Network Element State Connection\nElement: {element}\nState: {from_state}")
                        G.add_edge(element, 
                                 to_state,
                                 edge_type="element_state",
                                 color='rgba(0, 255, 0, 0.6)',  # Green with transparency
                                 description=f"Network Element State Connection\nElement: {element}\nState: {to_state}")

    # Improve layout with custom parameters
    pos = nx.spring_layout(G, k=2, iterations=100, scale=2.0)
    
    # Create separate edge traces for different edge types
    edge_traces = []
    arrow_traces = []
    
    # Group edges by type
    transition_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'transition']
    relationship_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'relationship']
    element_state_edges = [(u, v) for u, v, d in G.edges(data=True) if d['edge_type'] == 'element_state']
    
    # Create traces for transition edges (blue)
    if transition_edges:
        edge_x, edge_y, edge_descriptions = [], [], []
        arrow_x, arrow_y, arrow_descriptions = [], [], []
        
        for edge in transition_edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_descriptions.append(G.edges[edge]['description'])
            
            # Arrow position
            arrow_x.append(x0 + 0.7 * (x1 - x0))
            arrow_y.append(y0 + 0.7 * (y1 - y0))
            arrow_descriptions.append(G.edges[edge]['description'])
        
        edge_traces.append(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(0, 0, 255, 0.6)'),
            hoverinfo='text',
            text=edge_descriptions,
            mode='lines',
            name='State Transitions'
        ))
        
        arrow_traces.append(go.Scatter(
            x=arrow_x, y=arrow_y,
            mode='markers',
            marker=dict(
                symbol='triangle-right',
                size=8,
                color='rgba(0, 0, 255, 0.6)',
                angle=45,
            ),
            hoverinfo='text',
            text=arrow_descriptions,
            name='Transition Arrows'
        ))
    
    # Create traces for relationship edges (orange)
    if relationship_edges:
        edge_x, edge_y, edge_descriptions = [], [], []
        arrow_x, arrow_y, arrow_descriptions = [], [], []
        
        for edge in relationship_edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_descriptions.append(G.edges[edge]['description'])
            
            # Arrow position
            arrow_x.append(x0 + 0.7 * (x1 - x0))
            arrow_y.append(y0 + 0.7 * (y1 - y0))
            arrow_descriptions.append(G.edges[edge]['description'])
        
        edge_traces.append(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(255, 165, 0, 0.6)'),
            hoverinfo='text',
            text=edge_descriptions,
            mode='lines',
            name='Network Relationships'
        ))
        
        arrow_traces.append(go.Scatter(
            x=arrow_x, y=arrow_y,
            mode='markers',
            marker=dict(
                symbol='triangle-right',
                size=8,
                color='rgba(255, 165, 0, 0.6)',
                angle=45,
            ),
            hoverinfo='text',
            text=arrow_descriptions,
            name='Relationship Arrows'
        ))

    # Create traces for element-state edges (green)
    if element_state_edges:
        edge_x, edge_y, edge_descriptions = [], [], []
        arrow_x, arrow_y, arrow_descriptions = [], [], []
        
        for edge in element_state_edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_descriptions.append(G.edges[edge]['description'])
            
            # Arrow position
            arrow_x.append(x0 + 0.7 * (x1 - x0))
            arrow_y.append(y0 + 0.7 * (y1 - y0))
            arrow_descriptions.append(G.edges[edge]['description'])
        
        edge_traces.append(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='rgba(0, 255, 0, 0.6)'),
            hoverinfo='text',
            text=edge_descriptions,
            mode='lines',
            name='Element-State Connections'
        ))
        
        arrow_traces.append(go.Scatter(
            x=arrow_x, y=arrow_y,
            mode='markers',
            marker=dict(
                symbol='triangle-right',
                size=8,
                color='rgba(0, 255, 0, 0.6)',
                angle=45,
            ),
            hoverinfo='text',
            text=arrow_descriptions,
            name='Element-State Arrows'
        ))

    # Create node traces by type
    node_colors = {
        "state": ("lightblue", "darkblue", "circle"),
        "network_element": ("lightgreen", "darkgreen", "square")
    }

    # Create separate traces for each node type
    node_traces = []
    for node_type, (fill_color, line_color, symbol) in node_colors.items():
        nodes_x = []
        nodes_y = []
        nodes_text = []
        
        for node in G.nodes():
            if node_types.get(node) == node_type:
                x, y = pos[node]
                nodes_x.append(x)
                nodes_y.append(y)
                node_info = G.nodes[node]
                hover_text = f"{node}\nType: {node_info['type']}\n{node_info.get('description', '')}"
                nodes_text.append(hover_text)

        if nodes_x:  # Only create trace if there are nodes of this type
            node_trace = go.Scatter(
                x=nodes_x, y=nodes_y,
                mode='markers+text',
                hoverinfo='text',
                marker=dict(
                    showscale=False,
                    color=fill_color,
                    size=30,
                    symbol=symbol,
                    line=dict(width=2, color=line_color)
                ),
                text=[text.split('\n')[0] for text in nodes_text],
                textposition='bottom center',
                hovertext=nodes_text,
                name=node_type.replace('_', ' ').title()
            )
            node_traces.append(node_trace)

    # Create figure with improved layout
    fig = go.Figure(data=edge_traces + arrow_traces + node_traces,
                   layout=go.Layout(
                       showlegend=True,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       plot_bgcolor='white',
                       height=1000,  # Increased height
                       width=1400,  # Increased width
                       title={
                           'text': "5G Network Registration Procedure",
                           'y': 0.95,
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'
                       },
                       legend=dict(
                           yanchor="top",
                           y=0.99,
                           xanchor="left",
                           x=0.01,
                           bgcolor='rgba(255, 255, 255, 0.8)'
                       )
                   ))
    
    return fig, G, pos

fig, G, pos = create_plotly_graph(extracted_data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("5G Network Registration Procedure Visualization", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    dcc.Graph(
        id='network-graph',
        figure=fig,
        style={'height': '1000px'}  # Ensure the graph takes up enough space
    ),
], style={'backgroundColor': '#f8f9fa', 'padding': '20px'})

if __name__ == '__main__':
    app.run_server(debug=True)