from fastapi import FastAPI
from graph_router import router

app = FastAPI()

# Include the router
app.include_router(router)
