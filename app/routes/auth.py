from fastapi import APIRouter, HTTPException
from app.services.schema import User
from app.services.db import DatabaseSession
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(username: str, password: str, db: DatabaseSession):
    auth_service = AuthService(db)
    access_token = auth_service.login_user(username, password)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": access_token, "token_type": "bearer"}