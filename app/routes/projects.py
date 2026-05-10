from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated

from app.models import Project, ProjectCreate, ProjectUpdate, User
from app.services.project_service import ProjectService
from app.services.db import DatabaseSession
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/project",
    tags=["Projects"]
)

@router.get("/", response_model=List[Project])
def get_all_projects(db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Retrieve all projects from the database. Requires authentication."""
    return ProjectService.get_all_projects(db)

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Retrieve a specific project by its unique ID. Requires authentication."""
    return ProjectService.get_project(db, project_id)

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Create a new project. Requires authentication."""
    return ProjectService.create_project(db, project)

@router.patch("/{project_id}", response_model=Project)
def update_project(project_id: str, project_update: ProjectUpdate, db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Partially update an existing project. Requires authentication."""
    return ProjectService.update_project(db, project_id, project_update)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Remove a project from the database. Requires authentication."""
    return ProjectService.delete_project(db, project_id)