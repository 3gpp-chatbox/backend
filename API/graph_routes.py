from fastapi import APIRouter, HTTPException
import json
import os
import sys
from typing import Dict, List

router = APIRouter()

@router.get("/graphs/{procedure_name}")
async def get_graph_data(procedure_name: str):
    """Get graph data for a specific procedure"""
    try:
        # Construct path to graph file
        root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(root_folder)
        graph_path = os.path.join(
            "graphs", 
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
        graph_dir = os.path.join("backend", "graphs")
        graph_files = [
            f.replace("_graph.json", "")
            for f in os.listdir(graph_dir)
            if f.endswith("_graph.json")
        ]
        return {
            "status": "success",
            "data": graph_files
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing graphs: {str(e)}"
        )