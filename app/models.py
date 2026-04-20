from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import List, Optional

# /project route data models

class ProjectBase(BaseModel):
    title: str = Field(..., example="Deepfake Detection System")
    description: str = Field(..., example="A dual-stream CNN model using Vision Transformers.")
    tech_stack: List[str] = Field(..., example=["Python", "PyTorch", "FastAPI"])
    img_url: Optional[HttpUrl] = Field(None, example="https://example.com/project-image.png")
    github_url: Optional[HttpUrl] = Field(None, example="https://github.com/user/project")
    live_demo_url: Optional[HttpUrl] = Field(None, example="https://demo.com/project")

class ProjectCreate(ProjectBase):
    """Used for POST requests: All base fields are required."""
    pass

class ProjectUpdate(BaseModel):
    """Used for PATCH requests: All fields are optional so you can update just one part."""
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    img_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    live_demo_url: Optional[HttpUrl] = None

class Project(ProjectBase):
    """Used for GET responses: Includes the database ID."""
    id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    model_config = ConfigDict(from_attributes=True)