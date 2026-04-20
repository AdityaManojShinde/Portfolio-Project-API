from db import Base
from sqlalchemy import Column, String, Text, DateTime, JSON
from datetime import datetime
from uuid import uuid4

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    tech_stack = Column(JSON, nullable=True)  # Store skills as a JSON array
    github_link = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    live_demo_link = Column(String, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.now())