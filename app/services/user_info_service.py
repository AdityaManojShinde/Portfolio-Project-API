from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from datetime import datetime

from app.services.schema import UserInfo as UserInfoDB
from app.models import UserInfoCreate, UserInfoUpdate


class UserInfoService:
    """Service layer for UserInfo database operations."""

    @staticmethod
    def _convert_urls_to_strings(data: dict) -> dict:
        """Convert HttpUrl objects to strings for database storage."""
        url_fields = ["profile_img_url", "resume_url"]
        for field in url_fields:
            if field in data and data[field] is not None:
                data[field] = str(data[field])
        return data

    @staticmethod
    def create_or_update_user_info(
        db: Session, user_id: str, info_data: UserInfoCreate
    ) -> UserInfoDB:
        """Create or update user info."""
        try:
            user_info = (
                db.query(UserInfoDB).filter(UserInfoDB.user_id == user_id).first()
            )

            info_dict = info_data.model_dump(exclude_unset=True)
            info_dict = UserInfoService._convert_urls_to_strings(info_dict)

            if user_info:
                # Update existing
                for key, value in info_dict.items():
                    if hasattr(user_info, key):
                        setattr(user_info, key, value)
            else:
                # Create new
                info_dict["user_id"] = user_id
                user_info = UserInfoDB(**info_dict)
                db.add(user_info)

            db.commit()
            db.refresh(user_info)
            return user_info
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_user_info(db: Session, user_id: str) -> UserInfoDB:
        """Get user info by user_id."""
        user_info = db.query(UserInfoDB).filter(UserInfoDB.user_id == user_id).first()
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")
        return user_info

    @staticmethod
    def get_public_user_info(db: Session) -> UserInfoDB:
        """Get the first public user info record."""
        user_info = db.query(UserInfoDB).first()
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")
        return user_info

    @staticmethod
    def update_user_info(
        db: Session, user_id: str, update_data: UserInfoUpdate
    ) -> UserInfoDB:
        """Update user info."""
        try:
            user_info = (
                db.query(UserInfoDB).filter(UserInfoDB.user_id == user_id).first()
            )
            if not user_info:
                raise HTTPException(status_code=404, detail="User info not found")

            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict = UserInfoService._convert_urls_to_strings(update_dict)

            for key, value in update_dict.items():
                if hasattr(user_info, key):
                    setattr(user_info, key, value)

            db.commit()
            db.refresh(user_info)
            return user_info
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def delete_user_info(db: Session, user_id: str) -> None:
        """Delete user info."""
        try:
            user_info = (
                db.query(UserInfoDB).filter(UserInfoDB.user_id == user_id).first()
            )
            if not user_info:
                raise HTTPException(status_code=404, detail="User info not found")

            db.delete(user_info)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
