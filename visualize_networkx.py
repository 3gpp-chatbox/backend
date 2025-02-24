import networkx as nx
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import json

extracted_data = json.load(open("intermediate_results_95_783.json"))

def create_plotly_graph(data):
    G = nx.DiGraph()
    result = data["results"][0]

    for state in result["states"]:
        G.add_node(state["name"], type=state["type"], label=state["name"])

    for element in result["network_elements"]:
        G.add_node(element["name"], type=element["type"], label=element["name"])

    for transition in result["transitions"]:
        G.add_edge(transition["from_state"], transition["to_state"], trigger=transition["trigger"], description=transition["condition"])

    for relation in result["network_element_relationships"]:
        G.add_edge(relation["element1"], relation["element2"], relationship=relation["relationship"], description=relation["relationship"])

    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    edge_descriptions = [] #added
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_descriptions.append(G.edges[edge]['description']) #added

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='text', #changed
        text=edge_descriptions, #added
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(showscale=False, color='lightblue', size=15),
        text=node_text,
        textposition='bottom center')

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig, G, pos

fig, G, pos = create_plotly_graph(extracted_data)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='network-graph', figure=fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)