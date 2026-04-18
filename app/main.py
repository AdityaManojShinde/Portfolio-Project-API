from fastapi import FastAPI
import uvicorn

from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    """Root endpoint to verify that the API is working."""
    return {"message": "Hello, World!", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    # Use reload=True only in development for auto-reload on code changes
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True) 