from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.models import Contact, ContactCreate, ContactUpdate
from app.services.schema import User
from app.services.contact_service import ContactService
from app.services.db import DatabaseSession
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


@router.get("/", response_model=Contact)
def get_contact(db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Get current user's contact information."""
    return ContactService.get_contact(db, current_user.id)


@router.post("/", response_model=Contact)
def create_or_update_contact(
    contact: ContactCreate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Create or update contact information."""
    return ContactService.create_or_update_contact(db, current_user.id, contact)


@router.patch("/", response_model=Contact)
def update_contact(
    contact_update: ContactUpdate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Update specific fields of contact information."""
    return ContactService.update_contact(db, current_user.id, contact_update)


@router.delete("/")
def delete_contact(db: DatabaseSession, current_user: Annotated[User, Depends(get_current_user)]):
    """Delete contact information."""
    ContactService.delete_contact(db, current_user.id)
    return {"message": "Contact info deleted successfully"}
