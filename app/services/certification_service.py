from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.services.schema import Certification as CertificationDB
from app.models import CertificationCreate, CertificationUpdate


class CertificationService:
    """Service layer for Certification database operations."""

    @staticmethod
    def _convert_urls_to_strings(data: dict) -> dict:
        """Convert HttpUrl objects to strings for database storage."""
        url_fields = ["verification_url", "img_url", "pdf_url"]
        for field in url_fields:
            if field in data and data[field] is not None:
                data[field] = str(data[field])
        return data

    @staticmethod
    def create_certification(
        db: Session, user_id: str, certification_data: CertificationCreate
    ) -> CertificationDB:
        """Create a new certification entry."""
        try:
            certification_dict = certification_data.model_dump(exclude_unset=True)
            certification_dict = CertificationService._convert_urls_to_strings(
                certification_dict
            )
            certification_dict["user_id"] = user_id

            certification = CertificationDB(**certification_dict)
            db.add(certification)
            db.commit()
            db.refresh(certification)
            return certification
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_certification(db: Session, certification_id: str) -> CertificationDB:
        """Get certification by ID."""
        certification = (
            db.query(CertificationDB)
            .filter(CertificationDB.id == certification_id)
            .first()
        )
        if not certification:
            raise HTTPException(status_code=404, detail="Certification not found")
        return certification

    @staticmethod
    def get_user_certifications(db: Session, user_id: str) -> list[CertificationDB]:
        """Get all certifications for a user."""
        return (
            db.query(CertificationDB).filter(CertificationDB.user_id == user_id).all()
        )

    @staticmethod
    def get_all_certifications(db: Session) -> list[CertificationDB]:
        """Get all certifications."""
        return db.query(CertificationDB).all()

    @staticmethod
    def update_certification(
        db: Session, certification_id: str, update_data: CertificationUpdate
    ) -> CertificationDB:
        """Update certification entry."""
        try:
            certification = (
                db.query(CertificationDB)
                .filter(CertificationDB.id == certification_id)
                .first()
            )
            if not certification:
                raise HTTPException(status_code=404, detail="Certification not found")

            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict = CertificationService._convert_urls_to_strings(update_dict)

            for key, value in update_dict.items():
                if hasattr(certification, key):
                    setattr(certification, key, value)

            db.commit()
            db.refresh(certification)
            return certification
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def delete_certification(db: Session, certification_id: str) -> None:
        """Delete certification entry."""
        try:
            certification = (
                db.query(CertificationDB)
                .filter(CertificationDB.id == certification_id)
                .first()
            )
            if not certification:
                raise HTTPException(status_code=404, detail="Certification not found")

            db.delete(certification)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
