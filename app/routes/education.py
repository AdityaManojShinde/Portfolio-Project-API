from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated

from app.models import Education, EducationCreate, EducationUpdate
from app.services.schema import User
from app.services.education_service import EducationService
from app.services.db import DatabaseSession
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/education", tags=["Education"])


@router.get("/", response_model=List[Education])
def get_user_education(db: DatabaseSession):
    """Get all public education entries."""
    return EducationService.get_all_education(db)


@router.get("/{education_id}", response_model=Education)
def get_education(education_id: str, db: DatabaseSession):
    """Get a specific public education entry."""
    return EducationService.get_education(db, education_id)


@router.post("/", response_model=Education, status_code=201)
def create_education(
    education: EducationCreate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a new education entry."""
    return EducationService.create_education(db, current_user.id, education)


@router.patch("/{education_id}", response_model=Education)
def update_education(
    education_id: str,
    education_update: EducationUpdate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update a specific education entry."""
    education = EducationService.get_education(db, education_id)
    # Verify ownership
    if education.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this education record"
        )
    return EducationService.update_education(db, education_id, education_update)


@router.delete("/{education_id}")
def delete_education(
    education_id: str,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete an education entry."""
    education = EducationService.get_education(db, education_id)
    # Verify ownership
    if education.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this education record"
        )
    EducationService.delete_education(db, education_id)
    return {"message": "Education record deleted successfully"}
