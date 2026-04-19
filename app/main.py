from fastapi import FastAPI, Response
import uvicorn

from datetime import datetime
from app.routes import projects

app = FastAPI()

# Add Routes
app.include_router(projects.router)

@app.get("/")
def root():
    """Root endpoint to verify that the API is working."""
    return {"message": "Hello, World!", "timestamp": datetime.now().isoformat()}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 means "No Content"

