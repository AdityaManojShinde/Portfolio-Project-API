from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated

from app.models import Project, ProjectCreate, ProjectUpdate
from app.services.schema import User
from app.services.project_service import ProjectService
from app.services.db import DatabaseSession
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/project", tags=["Projects"])


@router.get("/", response_model=List[Project])
def get_user_projects(db: DatabaseSession):
    """Retrieve all public projects."""
    return ProjectService.get_all_projects(db)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str, db: DatabaseSession):
    """Retrieve a specific public project by its unique ID."""
    return ProjectService.get_project(db, project_id)


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a new project. Requires authentication."""
    return ProjectService.create_project(db, current_user.id, project)


@router.patch("/{project_id}", response_model=Project)
def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Partially update an existing project. Requires authentication."""
    project = ProjectService.get_project(db, project_id)
    # Verify ownership
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this project"
        )
    return ProjectService.update_project(db, project_id, project_update)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Remove a project from the database. Requires authentication."""
    project = ProjectService.get_project(db, project_id)
    # Verify ownership
    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this project"
        )
    ProjectService.delete_project(db, project_id)
