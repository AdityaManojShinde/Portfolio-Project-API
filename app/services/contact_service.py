from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.services.schema import Contact as ContactDB
from app.models import ContactCreate, ContactUpdate


class ContactService:
    """Service layer for Contact database operations."""

    @staticmethod
    def _convert_urls_to_strings(data: dict) -> dict:
        """Convert HttpUrl objects to strings for database storage."""
        url_fields = ["linkedin_url", "github_url"]
        for field in url_fields:
            if field in data and data[field] is not None:
                data[field] = str(data[field])
        return data

    @staticmethod
    def create_or_update_contact(
        db: Session, user_id: str, contact_data: ContactCreate
    ) -> ContactDB:
        """Create or update contact info."""
        try:
            contact = db.query(ContactDB).filter(ContactDB.user_id == user_id).first()

            contact_dict = contact_data.model_dump(exclude_unset=True)
            contact_dict = ContactService._convert_urls_to_strings(contact_dict)

            if contact:
                # Update existing
                for key, value in contact_dict.items():
                    if hasattr(contact, key):
                        setattr(contact, key, value)
            else:
                # Create new
                contact_dict["user_id"] = user_id
                contact = ContactDB(**contact_dict)
                db.add(contact)

            db.commit()
            db.refresh(contact)
            return contact
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_contact(db: Session, user_id: str) -> ContactDB:
        """Get contact by user_id."""
        contact = db.query(ContactDB).filter(ContactDB.user_id == user_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact info not found")
        return contact

    @staticmethod
    def get_public_contact(db: Session) -> ContactDB:
        """Get the first public contact information record."""
        contact = db.query(ContactDB).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact info not found")
        return contact

    @staticmethod
    def update_contact(
        db: Session, user_id: str, update_data: ContactUpdate
    ) -> ContactDB:
        """Update contact info."""
        try:
            contact = db.query(ContactDB).filter(ContactDB.user_id == user_id).first()
            if not contact:
                raise HTTPException(status_code=404, detail="Contact info not found")

            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict = ContactService._convert_urls_to_strings(update_dict)

            for key, value in update_dict.items():
                if hasattr(contact, key):
                    setattr(contact, key, value)

            db.commit()
            db.refresh(contact)
            return contact
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def delete_contact(db: Session, user_id: str) -> None:
        """Delete contact."""
        try:
            contact = db.query(ContactDB).filter(ContactDB.user_id == user_id).first()
            if not contact:
                raise HTTPException(status_code=404, detail="Contact info not found")

            db.delete(contact)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
