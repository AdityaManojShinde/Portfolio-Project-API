from sqlalchemy.orm import Session
from app.services.schema import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os
load_dotenv()


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
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