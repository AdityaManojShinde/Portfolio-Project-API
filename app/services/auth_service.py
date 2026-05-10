from sqlalchemy.orm import Session
from app.services.schema import User
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from dotenv import load_dotenv
import os
load_dotenv()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenData(BaseModel):
    username: str | None = None


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def login_user(self, username: str, password: str) -> str | None:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        access_token = self.create_access_token(data={"sub": user.username})
        return access_token
    
    def register_user(self, username: str, password: str) -> User:
        if self.db.query(User).filter(User.username == username).first():
            raise ValueError("Username already exists")
        hashed_password = self.hash_password(password)
        new_user = User(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def verify_token(self, token: str) -> str | None:
        """Verify JWT token and return username if valid"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
    
    def get_user_by_username(self, username: str) -> User | None:
        """Get user from database by username"""
        return self.db.query(User).filter(User.username == username).first()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Dependency to get current authenticated user from JWT token"""
    from app.services.db import DBSession
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    db = DBSession()
    try:
        auth_service = AuthService(db)
        username = auth_service.verify_token(token)
        
        if username is None:
            raise credentials_exception
        
        user = auth_service.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        
        return user
    finally:
        db.close()