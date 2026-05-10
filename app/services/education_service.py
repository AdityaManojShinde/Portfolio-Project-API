from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.services.schema import Education as EducationDB
from app.models import EducationCreate, EducationUpdate


class EducationService:
    """Service layer for Education database operations."""

    @staticmethod
    def create_education(db: Session, user_id: str, education_data: EducationCreate) -> EducationDB:
        """Create a new education entry."""
        try:
            education_dict = education_data.model_dump(exclude_unset=True)
            education_dict['user_id'] = user_id
            
            education = EducationDB(**education_dict)
            db.add(education)
            db.commit()
            db.refresh(education)
            return education
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_education(db: Session, education_id: str) -> EducationDB:
        """Get education by ID."""
        education = db.query(EducationDB).filter(EducationDB.id == education_id).first()
        if not education:
            raise HTTPException(status_code=404, detail="Education not found")
        return education

    @staticmethod
    def get_user_education(db: Session, user_id: str) -> list[EducationDB]:
        """Get all education entries for a user."""
        return db.query(EducationDB).filter(EducationDB.user_id == user_id).all()

    @staticmethod
    def update_education(db: Session, education_id: str, update_data: EducationUpdate) -> EducationDB:
        """Update education entry."""
        try:
            education = db.query(EducationDB).filter(EducationDB.id == education_id).first()
            if not education:
                raise HTTPException(status_code=404, detail="Education not found")
            
            update_dict = update_data.model_dump(exclude_unset=True)
            
            for key, value in update_dict.items():
                if hasattr(education, key):
                    setattr(education, key, value)
            
            db.commit()
            db.refresh(education)
            return education
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def delete_education(db: Session, education_id: str) -> None:
        """Delete education entry."""
        try:
            education = db.query(EducationDB).filter(EducationDB.id == education_id).first()
            if not education:
                raise HTTPException(status_code=404, detail="Education not found")
            
            db.delete(education)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
