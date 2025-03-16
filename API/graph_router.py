from fastapi import APIRouter, HTTPException
import json
import os
from typing import Dict, List

router = APIRouter()

def get_graphs_directory(result_set: str = None) -> str:
    """Get the absolute path to the graphs directory inside backend"""
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graphs_dir = os.path.join(backend_dir, "graphs")
    
    if result_set:
        # Create subdirectory for specific result set
        result_dir = os.path.join(graphs_dir, result_set)
        os.makedirs(result_dir, exist_ok=True)
        return result_dir
    
    # Create main graphs directory if it doesn't exist
    os.makedirs(graphs_dir, exist_ok=True)
    return graphs_dir

@router.get("/graphs/result-sets/{result_set}/{procedure_name}")
async def get_graph_data(result_set: str, procedure_name: str):
    """Get graph data for a specific procedure from a result set"""
    try:
        graphs_dir = get_graphs_directory(result_set)
        graph_path = os.path.join(
            graphs_dir,
            f"{procedure_name.lower()}.json"
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
            detail=f"Graph data not found for {procedure_name} in {result_set}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading graph data: {str(e)}"
        )

@router.get("/graphs/result-sets")
async def list_result_sets():
    """List all available result sets"""
    try:
        graphs_dir = get_graphs_directory()
        result_sets = [
            d for d in os.listdir(graphs_dir)
            if os.path.isdir(os.path.join(graphs_dir, d))
        ]
        
        return {
            "status": "success",
            "data": result_sets,
            "message": f"Found {len(result_sets)} result sets"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing result sets: {str(e)}"
        )

@router.get("/graphs/result-sets/{result_set}")
async def list_available_graphs(result_set: str):
    """List all available graph files in a result set"""
    try:
        graphs_dir = get_graphs_directory(result_set)
        
        # List all graph files
        graph_files = [
            f.replace(".json", "")
            for f in os.listdir(graphs_dir)
            if f.endswith(".json")
        ]
        
        return {
            "status": "success",
            "data": graph_files,
            "message": f"Found {len(graph_files)} graph files in {result_set}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing graphs: {str(e)}"
        )