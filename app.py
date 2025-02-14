from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Neo4jConnection, ChromaDBConnection

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize connections
neo4j = Neo4jConnection()
chroma = ChromaDBConnection()

@app.get("/")
async def root():
    return "Frontend and backend connected!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
