from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


# ============ User Models ============
class UserResponse(BaseModel):
    id: str
    username: str
    model_config = ConfigDict(from_attributes=True)


# ============ UserInfo Models ============
class UserInfoBase(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    profile_img_url: Optional[HttpUrl] = Field(None, example="https://example.com/profile.png")
    bio: Optional[str] = Field(None, example="Software developer with a passion for AI.")
    resume_url: Optional[HttpUrl] = Field(None, example="https://example.com/resume.pdf")


class UserInfoCreate(UserInfoBase):
    pass


class UserInfoUpdate(BaseModel):
    name: Optional[str] = None
    profile_img_url: Optional[HttpUrl] = None
    bio: Optional[str] = None
    resume_url: Optional[HttpUrl] = None


class UserInfo(UserInfoBase):
    id: str
    user_id: str
    model_config = ConfigDict(from_attributes=True)


# ============ Contact Models ============
class ContactBase(BaseModel):
    email: Optional[str] = Field(None, example="user@example.com")
    phone_number: Optional[str] = Field(None, example="+1234567890")
    whatsapp_number: Optional[str] = Field(None, example="+1234567890")
    linkedin_url: Optional[HttpUrl] = Field(None, example="https://linkedin.com/in/user")
    github_url: Optional[HttpUrl] = Field(None, example="https://github.com/user")


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None


class Contact(ContactBase):
    id: str
    user_id: str
    model_config = ConfigDict(from_attributes=True)


# ============ Project Models ============
class ProjectBase(BaseModel):
    title: str = Field(..., example="Deepfake Detection System")
    description: Optional[str] = Field(None, example="A dual-stream CNN model using Vision Transformers.")
    tech_stack: Optional[List[str]] = Field(None, example=["Python", "PyTorch", "FastAPI"])
    image_url: Optional[HttpUrl] = Field(None, example="https://example.com/project-image.png")
    github_link: Optional[HttpUrl] = Field(None, example="https://github.com/user/project")
    video_link: Optional[HttpUrl] = Field(None, example="https://youtube.com/watch?v=xyz")
    live_demo_link: Optional[HttpUrl] = Field(None, example="https://demo.com/project")
    is_featured: Optional[bool] = Field(False, example=False)
    order_index: Optional[int] = Field(0, example=0)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    image_url: Optional[HttpUrl] = None
    github_link: Optional[HttpUrl] = None
    video_link: Optional[HttpUrl] = None
    live_demo_link: Optional[HttpUrl] = None
    is_featured: Optional[bool] = None
    order_index: Optional[int] = None


class Project(ProjectBase):
    id: str
    user_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ============ Education Models ============
class EducationBase(BaseModel):
    institution_name: Optional[str] = Field(None, example="MIT")
    degree: Optional[str] = Field(None, example="Bachelor of Science")
    field_of_study: Optional[str] = Field(None, example="Computer Science")
    start_date: Optional[datetime] = Field(None, example="2020-09-01")
    end_date: Optional[datetime] = Field(None, example="2024-05-31")


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution_name: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Education(EducationBase):
    id: str
    user_id: str
    model_config = ConfigDict(from_attributes=True)


# ============ Certification Models ============
class CertificationBase(BaseModel):
    name: Optional[str] = Field(None, example="AWS Certified Solutions Architect")
    issuing_organization: Optional[str] = Field(None, example="Amazon Web Services")
    verification_url: Optional[HttpUrl] = Field(None, example="https://aws.amazon.com/verify/123")
    img_url: Optional[HttpUrl] = Field(None, example="https://example.com/cert.png")
    pdf_url: Optional[HttpUrl] = Field(None, example="https://example.com/cert.pdf")
    issue_date: Optional[datetime] = Field(None, example="2023-01-15")
    expiration_date: Optional[datetime] = Field(None, example="2025-01-15")


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    verification_url: Optional[HttpUrl] = None
    img_url: Optional[HttpUrl] = None
    pdf_url: Optional[HttpUrl] = None
    issue_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None


class Certification(CertificationBase):
    id: str
    user_id: str
    model_config = ConfigDict(from_attributes=True)


# ============ Auth Models ============
class LoginRequest(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(..., example="strongpassword")


class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., example="bearer")