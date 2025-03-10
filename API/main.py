from fastapi import FastAPI
from graph_router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define allowed origins (frontend URL)
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000"   # Alternative local frontend
]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the router
app.include_router(router)

