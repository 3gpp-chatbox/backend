from fastapi import APIRouter, HTTPException
import json
import os
from typing import Dict, List

router = APIRouter()

def get_graphs_directory() -> str:
    """Get the absolute path to the graphs directory inside backend"""
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graphs_dir = os.path.join(backend_dir, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    
    return graphs_dir

@router.get("/graphs/{procedure_name}")
async def get_graph_data(procedure_name: str):
    """Get graph data for a specific procedure"""
    try:
        graphs_dir = get_graphs_directory()
        graph_path = os.path.join(
            graphs_dir,
            f"{procedure_name.lower().replace(' ', '_')}_graph.json"
        )
        
        # Read graph data
        with open(graph_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
            
        return {
            "status": "success",
            "data": graph_data
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail=f"Graph data not found for {procedure_name}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading graph data: {str(e)}"
        )

@router.get("/graphs")
async def list_available_graphs():
    """List all available graph files"""
    try:
        graphs_dir = get_graphs_directory()
        
        # List all graph files
        graph_files = [
            f.replace("_graph.json", "")
            for f in os.listdir(graphs_dir)
            if f.endswith("_graph.json")
        ]
        
        return {
            "status": "success",
            "data": graph_files,
            "message": f"Found {len(graph_files)} graph files"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing graphs: {str(e)}"
        )