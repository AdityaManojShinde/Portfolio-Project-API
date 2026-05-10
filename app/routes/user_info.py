from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.models import UserInfo, UserInfoCreate, UserInfoUpdate
from app.services.schema import User
from app.services.user_info_service import UserInfoService
from app.services.db import DatabaseSession
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/user-info",
    tags=["User Info"]
)


@router.get("/", response_model=UserInfo)
def get_user_info(db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Get current user's profile information."""
    return UserInfoService.get_user_info(db, current_user.id)


@router.post("/", response_model=UserInfo)
def create_or_update_user_info(
    user_info: UserInfoCreate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Create or update user profile information."""
    return UserInfoService.create_or_update_user_info(db, current_user.id, user_info)


@router.patch("/", response_model=UserInfo)
def update_user_info(
    user_info_update: UserInfoUpdate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Update specific fields of user profile."""
    return UserInfoService.update_user_info(db, current_user.id, user_info_update)


@router.delete("/")
def delete_user_info(db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Delete user profile information."""
    UserInfoService.delete_user_info(db, current_user.id)
    return {"message": "User info deleted successfully"}
