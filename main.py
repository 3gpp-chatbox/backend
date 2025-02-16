from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from docx import Document
import os
import sqlite3
import json
from typing import Dict, List
from extract_procedures.graph_extractor import GraphExtractor

# Create FastAPI app instance
app = FastAPI(
    title="3GPP Procedures API",
    description="API for managing and visualizing 3GPP procedures",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GraphExtractor
extractor = GraphExtractor(db_path="nas_chunks.db")

@app.get("/")
async def root():
    return {"message": "Welcome to 3GPP Procedures API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/process-directory/{dir_name}")
async def process_directory(dir_name: str):
    """
    Process all .docx files in a specified directory
    """
    try:
        base_dir = "3GPP_Documents"
        spec_dir = os.path.join(base_dir, dir_name)
        
        if not os.path.exists(spec_dir):
            raise HTTPException(status_code=404, detail=f"Directory {spec_dir} does not exist")
        
        docx_files = [f for f in os.listdir(spec_dir) if f.endswith('.docx')]
        
        if not docx_files:
            raise HTTPException(status_code=404, detail=f"No .docx files found in {spec_dir}")
        
        results = []
        for docx_file in docx_files:
            docx_path = os.path.join(spec_dir, docx_file)
            print(f"Processing document: {docx_path}")
            
            try:
                doc = Document(docx_path)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                nodes, edges = extractor.process_text_in_chunks(text)
                
                # Get summary for this file
                summary = {
                    "filename": docx_file,
                    "text_length": len(text),
                    "nodes_count": {k: len(v) for k, v in nodes.items()},
                    "edges_count": len(edges),
                    "nodes": {k: list(v) for k, v in nodes.items()},
                    "edges": edges
                }
                results.append(summary)
                
            except Exception as e:
                print(f"Error processing {docx_file}: {str(e)}")
                results.append({
                    "filename": docx_file,
                    "error": str(e)
                })
        
        return JSONResponse({
            "directory": dir_name,
            "total_files": len(docx_files),
            "processed_files": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary")
async def get_summary():
    """
    Get a summary of all processed data
    """
    try:
        # Get database summary
        conn = sqlite3.connect(extractor.db_path)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM chunk_results')
        total_chunks = c.fetchone()[0]
        conn.close()
        
        # Get current nodes and edges
        nodes = {k: list(v) for k, v in extractor.nas_nodes.items()}
        edges = extractor.nas_edges
        
        # Create detailed summary
        summary = {
            "database_stats": {
                "total_chunks": total_chunks
            },
            "extraction_stats": {
                "total_nodes": sum(len(v) for v in nodes.values()),
                "nodes_by_type": {k: len(v) for k, v in nodes.items()},
                "total_edges": len(edges)
            },
            "nodes": nodes,
            "edges": edges
        }
        
        # Print summary to console
        print("\nNAS Graph Elements Summary:")
        for node_type, node_list in nodes.items():
            print(f"\n{node_type.capitalize()} ({len(node_list)}):")
            print('\n'.join(f"- {node}" for node in node_list))
        
        print("\nEdges:")
        for edge in edges:
            print(f"{edge['source']} --[{edge['relationship']}]--> {edge['target']} (Procedure: {edge['procedure']})")
        
        return JSONResponse(summary)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view-database")
async def view_database():
    """
    View all stored chunks and their extracted information from the database
    """
    try:
        conn = sqlite3.connect(extractor.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM chunk_results')
        rows = c.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "chunk_text": row[1],
                "nodes": json.loads(row[2]),
                "edges": json.loads(row[3])
            })
        
        return JSONResponse({
            "total_chunks": len(results),
            "chunks": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-procedures")
async def extract_procedures(file: UploadFile = File(...)):
    """
    Extract procedures from an uploaded .docx file
    """
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    
    try:
        # Save the uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        print(f"Processing file: {file.filename}")
        
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from the document
        doc = Document(temp_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        print(f"Extracted text length: {len(text)} characters")
        
        # Process the text using GraphExtractor
        print("Starting text processing...")
        nodes, edges = extractor.process_text_in_chunks(text)
        
        # Print summary of extracted data
        print("\nExtraction Summary:")
        print(f"Total nodes: {sum(len(v) for v in nodes.values())}")
        for node_type, values in nodes.items():
            print(f"- {node_type}: {len(values)} items")
        print(f"Total edges: {len(edges)}")
        
        # Convert sets to lists for JSON serialization
        nodes_json = {k: list(v) for k, v in nodes.items()}
        
        # Clean up temporary file
        os.remove(temp_path)
        print("Processing completed successfully")
        
        return JSONResponse({
            "nodes": nodes_json,
            "edges": edges
        })
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/procedures")
async def get_procedures():
    """
    Get all extracted procedures from the database
    """
    try:
        return {
            "nodes": {k: list(v) for k, v in extractor.nas_nodes.items()},
            "edges": extractor.nas_edges
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
