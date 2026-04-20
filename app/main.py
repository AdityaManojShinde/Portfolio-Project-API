from fastapi import FastAPI, Response
from datetime import datetime
from app.routes import projects
from app.services.db import Base, engine


app = FastAPI()

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Add Routes
app.include_router(projects.router)

@app.get("/")
def root():
    """Root endpoint to verify that the API is working."""
    return {"message": "Hello, World!", "timestamp": datetime.now().isoformat()}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 means "No Content"

