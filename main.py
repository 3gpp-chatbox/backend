from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables
load_dotenv()

# Neo4j Configuration
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

app = FastAPI(
    title="Periodic Registration API",
    description="API for querying 5G NAS Periodic Registration procedures",
    version="1.0.0"
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint showing available routes"""
    return {
        "status": "success",
        "message": "Periodic Registration API is running",
        "available_endpoints": {
            "all_procedures": "/periodic-registration",
            "api_endpoint": "/api/periodic-registration",
            "specific_trigger": "/periodic-registration/{trigger_id}",
            "rat_change": "/periodic-registration/change-in-rat-path"
        },
        "documentation": "/docs"  # FastAPI automatic documentation
    }

@app.get("/periodic-registration")
async def get_all_periodic_registration():
    """Get a list of all periodic registration procedures"""
    try:
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        with driver.session() as session:
            result = session.run("""
                MATCH (t:Trigger)
                WHERE t.type = 'Periodic_Registration'
                RETURN collect(t.name) as triggers
            """)
            data = result.single()
            return {
                "status": "success",
                "triggers": data["triggers"] if data else []
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'driver' in locals():
            driver.close()

@app.get("/api/periodic-registration")
async def get_periodic_registration():
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    
    try:
        with driver.session() as session:
            result = session.run("""
                MATCH (source:NetworkElement)-[r:SENDS_MESSAGE]->(dest:NetworkElement)
                WHERE r.procedure = 'Periodic_Registration'
                WITH r.trigger as trigger, collect({
                    source: source.name,
                    target: dest.name,
                    label: r.name,
                    step_number: r.step_number,
                    description: r.description
                }) as steps
                RETURN {
                    trigger: trigger,
                    steps: steps
                } as flow
                ORDER BY trigger
            """)
            
            flows = [record["flow"] for record in result]
            return {"flows": flows}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.close()

@app.get("/periodic-registration/{trigger_id}")
async def get_periodic_registration_trigger(trigger_id: str):
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    
    try:
        with driver.session() as session:
            trigger_name = trigger_id.replace('_', ' ')
            print(f"Looking for trigger: {trigger_name}")
            
            result = session.run("""
                MATCH (source:NetworkElement)-[r:SENDS_MESSAGE]->(dest:NetworkElement)
                WHERE r.procedure = 'Periodic_Registration'
                AND r.trigger = $trigger
                WITH source, dest, r
                ORDER BY r.step_number
                RETURN {
                    nodes: collect(DISTINCT {
                        id: source.name,
                        label: source.name,
                        type: 'NetworkElement',
                        description: coalesce(source.description, '')
                    }) + collect(DISTINCT {
                        id: dest.name,
                        label: dest.name,
                        type: 'NetworkElement',
                        description: coalesce(dest.description, '')
                    }),
                    edges: collect({
                        source: source.name,
                        target: dest.name,
                        label: coalesce(r.name, 'Message'),
                        description: coalesce(r.description, ''),
                        step_number: r.step_number,
                        message_type: coalesce(r.message_type, 'NAS Message')
                    }),
                    metadata: {
                        procedureName: 'Periodic Registration Update',
                        triggerName: $trigger,
                        specReference: '3GPP TS 24.501',
                        protocol: '5G NAS'
                    }
                } as response
            """, {"trigger": trigger_name})
            
            data = result.single()
            if not data:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No data found for trigger: {trigger_id}"
                )
            
            # Clean up the nodes to remove duplicates
            response_data = data["response"]
            if "nodes" in response_data:
                seen = set()
                unique_nodes = []
                for node in response_data["nodes"]:
                    if node["id"] not in seen:
                        seen.add(node["id"])
                        unique_nodes.append(node)
                response_data["nodes"] = unique_nodes
            
            print("Returning data structure:", response_data)  # Debug print
            return response_data
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
    finally:
        driver.close()

# Special endpoint for Change in RAT
@app.get("/periodic-registration/change-in-rat-path")
async def get_change_in_rat_path():
    return await get_periodic_registration_trigger("Change_in_RAT")

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True) 