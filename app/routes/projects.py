from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models import Project, ProjectCreate, ProjectUpdate 
from app.services.project_service import ProjectService
from app.services.db import DatabaseSession

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("/", response_model=List[Project])
def get_all_projects(db: DatabaseSession):
    """Retrieve all projects from the database."""
    return ProjectService.get_all_projects(db)

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, db: DatabaseSession):
    """Retrieve a specific project by its unique ID."""
    return ProjectService.get_project(db, project_id)

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: DatabaseSession):
    """Create a new project."""
    return ProjectService.create_project(db, project)

@router.patch("/{project_id}", response_model=Project)
def update_project(project_id: str, project_update: ProjectUpdate, db: DatabaseSession):
    """Partially update an existing project."""
    return ProjectService.update_project(db, project_id, project_update)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: DatabaseSession):
    """Remove a project from the database."""
    return ProjectService.delete_project(db, project_id)