import json

def split_edges_only(graph_data, edges_per_chunk=10):
    """
    Splits only the 'edges' part of the Flow Property Graph JSON into chunks of 10.
    'nodes' part is excluded (assumed to be validated separately).
    
    Parameters:
    - graph_data (dict): Original FPG JSON containing 'nodes' and 'edges'
    - edges_per_chunk (int): Number of edges per chunk

    Returns:
    - List[List[dict]]: A list of edge chunks, each containing only edges directly (no wrapping 'edges' key)
    """
    all_edges = graph_data.get("edges", [])
    if not all_edges:
        raise ValueError("No edges found in the provided data!")

    chunks = []
    for i in range(0, len(all_edges), edges_per_chunk):
        # Just append the list of edges directly without wrapping in 'edges' key
        chunk = all_edges[i:i+edges_per_chunk]
        chunks.append(chunk)

    return chunks

# Example usage
try:
    with open("step1.json") as f:
        fpg = json.load(f)

    edge_chunks = split_edges_only(fpg, edges_per_chunk=10)

    # Write each chunk of edges directly to files
    for idx, chunk in enumerate(edge_chunks, 1):
        with open(f"edges_batch_{idx}.json", "w") as f:
            json.dump(chunk, f, indent=2)
    print(f"Successfully split {len(edge_chunks)} chunks.")

except FileNotFoundError:
    print("The file 'step1.json' was not found.")
except json.JSONDecodeError:
    print("Error reading the JSON file.")
except ValueError as e:
    print(f"Error: {e}")

