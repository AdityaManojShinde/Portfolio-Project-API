from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.services.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Relationships
    info = relationship("UserInfo", back_populates="user", uselist=False, cascade="all, delete-orphan")
    contact = relationship("Contact", back_populates="user", uselist=False, cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="user", cascade="all, delete-orphan")

class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    profile_img_url = Column(String)
    bio = Column(Text)
    resume_url = Column(String)

    user = relationship("User", back_populates="info")

class Contact(Base):
    __tablename__ = "contact"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    email = Column(String)
    phone_number = Column(String)
    whatsapp_number = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)

    user = relationship("User", back_populates="contact")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    tech_stack = Column(JSON)  # e.g., ["Python", "FastAPI", "React"]
    github_link = Column(String)
    image_url = Column(String)
    video_link = Column(String)
    live_demo_link = Column(String)
    is_featured = Column(Boolean, default=False)
    order_index = Column(Integer, default=0) # Helps in manual sorting
    
    # Note: Using datetime.utcnow (no parens) so it executes on insertion
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="projects")

class Education(Base):
    __tablename__ = "education"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    institution_name = Column(String)
    degree = Column(String)
    field_of_study = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True) # Nullable for "Present"

    user = relationship("User", back_populates="education")

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    issuing_organization = Column(String)
    verification_url = Column(String)
    img_url = Column(String)
    pdf_url = Column(String)
    issue_date = Column(DateTime)
    expiration_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="certifications")