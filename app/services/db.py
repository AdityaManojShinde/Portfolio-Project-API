from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Annotated

DB_URL = "sqlite:///./project_db.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get a database session."""
    db = Session()
    try:
        yield db
    finally:
        db.close()

DatabaseSession = Annotated[Session, Depends(get_db)]
