from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.services.schema import Project  # SQLAlchemy model
from app.models import ProjectCreate, ProjectUpdate  # Pydantic models

class ProjectService:
    """Service layer for handling project-related database operations."""

    @staticmethod
    def create_project(db: Session, project_data: ProjectCreate) -> Project:
        """Create a new project in the database."""
        try:
            new_project = Project(**project_data.model_dump())  # Convert Pydantic model to SQLAlchemy model
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            return new_project
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_project(db: Session, project_id: str) -> Project:
        """Retrieve a project by its ID."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    @staticmethod
    def update_project(db: Session, project_id: str, update_data: ProjectUpdate) -> Project:
        """Update an existing project with new data."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_dict = update_data.model_dump(exclude_unset=True)  # Only update provided fields
        for key, value in update_dict.items():
            if hasattr(project, key):  # Safety check
                setattr(project, key, value)
        
        try:
            db.commit()
            db.refresh(project)
            return project
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

    @staticmethod
    def get_all_projects(db: Session) -> list[Project]:
        """Retrieve all projects."""
        return db.query(Project).all()
    
    @staticmethod
    def delete_project(db: Session, project_id: str) -> None:
        """Delete a project by its ID."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        try:
            db.delete(project)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
        

