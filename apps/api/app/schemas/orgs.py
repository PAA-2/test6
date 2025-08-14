from datetime import datetime
from pydantic import BaseModel, EmailStr


class OrganizationCreate(BaseModel):
    name: str


class OrganizationRead(OrganizationCreate):
    id: str
    slug: str | None = None
    logo_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrgInviteCreate(BaseModel):
    email: EmailStr
    role: str = "member"


class OrgInviteRead(BaseModel):
    token: str
    email: EmailStr
    role: str


class OrgSelect(BaseModel):
    org_id: str
