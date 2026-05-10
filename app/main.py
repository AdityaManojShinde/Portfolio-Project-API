from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from datetime import datetime
import os
from dotenv import load_dotenv
from app.routes import projects
from app.services.auth_service import AuthService
from app.services.db import Base, engine, DBSession
from app.routes import auth

# Load environment variables
load_dotenv()

# Validate required environment variables at startup
def _validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = ["SECRET_KEY","USERNAME", "PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            f"Please set them in your .env file or environment before starting the application."
        )

_validate_environment()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting application...")
    Base.metadata.create_all(bind=engine)
    
    # Create default user on startup (only if it doesn't already exist)
    db = DBSession()
    try:
        auth_service = AuthService(db)
        auth_service.register_user(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        print("✅ Default user created")
    except ValueError as e:
        if "already exists" in str(e):
            print("✅ Default user already exists")
        else:
            raise
    finally:
        db.close()
    
    yield  # Application runs here
    
    # Shutdown
    print("Shutting down application...")

app = FastAPI(lifespan=lifespan)

# Add Routes
app.include_router(projects.router)
app.include_router(auth.router)

@app.get("/")
def root():
    """Root endpoint to verify that the API is working."""
    return {"message": "Hello, World!", "timestamp": datetime.now().isoformat()}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 means "No Content"

