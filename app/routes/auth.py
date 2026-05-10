from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel

from app.services.auth_service import AuthService, get_current_user, oauth2_scheme
from app.services.db import DatabaseSession
from app.models import User


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str
    
    class Config:
        from_attributes = True


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DatabaseSession):
    """Authenticate user and return JWT token"""
    auth_service = AuthService(db)
    access_token = auth_service.login_user(form_data.username, form_data.password)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    """Get current authenticated user info"""
    return current_user