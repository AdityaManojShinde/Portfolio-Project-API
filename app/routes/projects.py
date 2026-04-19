from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models import Project, ProjectCreate, ProjectUpdate 

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

# Temporary in-memory database
proj_data = [
    {
        "id": 1,
        "title": "Dual-Stream Deepfake Detection",
        "description": "A high-accuracy detection system utilizing Vision Transformers (ViT) and SRM filters.",
        "tech_stack": ["Python", "PyTorch", "FastAPI"],
        "img_url": "https://raw.githubusercontent.com/AdityaManojShinde/assets/main/deepfake-detect.png",
        "github_url": "https://github.com/AdityaManojShinde/Deepfake-Detection",
        "live_demo_url": "https://deepfake-check.aditya.dev"
    },
    {
        "id": 2,
        "title": "Shoefy E-Commerce",
        "description": "A full-stack e-commerce platform for sneaker enthusiasts.",
        "tech_stack": ["PHP", "MySQL", "JavaScript"],
        "img_url": "https://raw.githubusercontent.com/AdityaManojShinde/assets/main/shoefy-preview.png",
        "github_url": "https://github.com/AdityaManojShinde/Shoefy",
        "live_demo_url": None
    }
]

@router.get("/", response_model=List[Project])
def get_all_projects():
    """Retrieve all projects from the database."""
    return proj_data

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int):
    """Retrieve a specific project by its unique ID."""
    project = next((p for p in proj_data if p["id"] == project_id), None)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Project with ID {project_id} not found"
        )
    return project

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):
    """Create a new project and assign a unique ID."""
    new_project = project.model_dump()
    
    # Logic to find the next available ID
    new_id = max(p["id"] for p in proj_data) + 1 if proj_data else 1
    new_project["id"] = new_id
    
    proj_data.append(new_project)
    return new_project

@router.patch("/{project_id}", response_model=Project)
def update_project(project_id: int, project_update: ProjectUpdate):
    """Partially update an existing project using PATCH."""
    # 1. Find the project
    project = next((p for p in proj_data if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 2. Extract only the fields the user actually sent
    update_data = project_update.model_dump(exclude_unset=True)
    
    # 3. Apply updates to the dictionary
    for key, value in update_data.items():
        project[key] = value
    
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    """Remove a project from the database."""
    global proj_data
    
    # Check if project exists before "deleting"
    project_exists = any(p["id"] == project_id for p in proj_data)
    if not project_exists:
        raise HTTPException(status_code=404, detail="Project not found")
    
    proj_data = [p for p in proj_data if p["id"] != project_id]
    # 204 No Content doesn't return a body, so we just return None
    return None