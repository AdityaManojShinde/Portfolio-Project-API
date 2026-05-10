from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import List, Optional


# User
class User(BaseModel):
    email: str = Field(..., example="user123@example.com")
    hashed_password: str = Field(..., example="$2b$12$KIXQu1e5s8v1Z6a9b8uOeG5j")

class UserInfo(BaseModel):
    name: Optional[str] = Field(None, example="user123")
    profile_img_url: Optional[HttpUrl] = Field(None, example="https://example.com/profile-image.png")
    bio: Optional[str] = Field(None, example="Software developer with a passion for AI and open-source projects.")


# /project route data models

class ProjectBase(BaseModel):
    title: str = Field(..., example="Deepfake Detection System")
    description: str = Field(..., example="A dual-stream CNN model using Vision Transformers.")
    tech_stack: List[str] = Field(..., example=["Python", "PyTorch", "FastAPI"])
    image_url: Optional[HttpUrl] = Field(None, example="https://example.com/project-image.png")
    github_link: Optional[HttpUrl] = Field(None, example="https://github.com/user/project")
    live_demo_link: Optional[HttpUrl] = Field(None, example="https://demo.com/project")

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


# /auth route data models

class LoginRequest(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(..., example="strongpassword")

class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., example="bearer")