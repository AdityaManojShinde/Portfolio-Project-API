from fastapi import APIRouter, Depends, HTTPException
from typing import List, Annotated

from app.models import Certification, CertificationCreate, CertificationUpdate
from app.services.schema import User
from app.services.certification_service import CertificationService
from app.services.db import DatabaseSession
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/certification", tags=["Certifications"])


@router.get("/", response_model=List[Certification])
def get_user_certifications(db: DatabaseSession):
    """Get all public certifications."""
    return CertificationService.get_all_certifications(db)


@router.get("/{certification_id}", response_model=Certification)
def get_certification(certification_id: str, db: DatabaseSession):
    """Get a specific public certification."""
    return CertificationService.get_certification(db, certification_id)


@router.post("/", response_model=Certification, status_code=201)
def create_certification(
    certification: CertificationCreate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a new certification entry."""
    return CertificationService.create_certification(db, current_user.id, certification)


@router.patch("/{certification_id}", response_model=Certification)
def update_certification(
    certification_id: str,
    certification_update: CertificationUpdate,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update a specific certification."""
    certification = CertificationService.get_certification(db, certification_id)
    # Verify ownership
    if certification.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this certification"
        )
    return CertificationService.update_certification(
        db, certification_id, certification_update
    )


@router.delete("/{certification_id}")
def delete_certification(
    certification_id: str,
    db: DatabaseSession,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete a certification."""
    certification = CertificationService.get_certification(db, certification_id)
    # Verify ownership
    if certification.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this certification"
        )
    CertificationService.delete_certification(db, certification_id)
    return {"message": "Certification deleted successfully"}
