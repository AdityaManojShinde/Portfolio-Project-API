from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime

from app.services.schema import Project as ProjectDB
from app.models import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service layer for handling project-related database operations."""

    @staticmethod
    def _convert_urls_to_strings(data: dict) -> dict:
        """Convert HttpUrl objects to strings for database storage."""
        url_fields = ['github_link', 'image_url', 'video_link', 'live_demo_link']
        for field in url_fields:
            if field in data and data[field] is not None:
                data[field] = str(data[field])
        return data

    @staticmethod
    def create_project(db: Session, user_id: str, project_data: ProjectCreate) -> ProjectDB:
        """Create a new project in the database."""
        try:
            project_dict = project_data.model_dump(exclude_unset=True)
            project_dict = ProjectService._convert_urls_to_strings(project_dict)
            project_dict['user_id'] = user_id
            project_dict['created_at'] = datetime.utcnow()
            project_dict['updated_at'] = datetime.utcnow()
            
            new_project = ProjectDB(**project_dict)
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            return new_project
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_project(db: Session, project_id: str) -> ProjectDB:
        """Retrieve a project by its ID."""
        project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    @staticmethod
    def get_user_projects(db: Session, user_id: str) -> list[ProjectDB]:
        """Retrieve all projects for a user."""
        return db.query(ProjectDB).filter(ProjectDB.user_id == user_id).order_by(ProjectDB.order_index).all()

    @staticmethod
    def get_all_projects(db: Session) -> list[ProjectDB]:
        """Retrieve all projects."""
        return db.query(ProjectDB).all()

    @staticmethod
    def update_project(db: Session, project_id: str, update_data: ProjectUpdate) -> ProjectDB:
        """Update an existing project with new data."""
        try:
            project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict = ProjectService._convert_urls_to_strings(update_dict)
            update_dict['updated_at'] = datetime.utcnow()
            
            for key, value in update_dict.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            
            db.commit()
            db.refresh(project)
            return project
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

    @staticmethod
    def delete_project(db: Session, project_id: str) -> None:
        """Delete a project by its ID."""
        try:
            project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            
            db.delete(project)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
        

