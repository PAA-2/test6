from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.orgs import (
    OrganizationCreate,
    OrganizationRead,
    OrgInviteCreate,
    OrgInviteRead,
)
from app.services import orgs as org_service

router = APIRouter(prefix="/orgs", tags=["orgs"])


@router.post("", response_model=OrganizationRead)
def create_org_endpoint(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    org = org_service.create_org(db, current_user, data.name)
    return OrganizationRead.from_orm(org)


@router.get("", response_model=list[OrganizationRead])
def list_orgs_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orgs = org_service.list_orgs(db, current_user)
    return [OrganizationRead.from_orm(o) for o in orgs]


@router.get("/{org_id}", response_model=OrganizationRead)
def get_org(
    org_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orgs = org_service.list_orgs(db, current_user)
    for o in orgs:
        if o.id == org_id:
            return OrganizationRead.from_orm(o)
    raise HTTPException(status_code=404, detail="Not found")


@router.get("/{org_id}/members")
def list_members(
    org_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        org_service.ensure_org_admin(db, current_user, org_id)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not allowed")
    members = org_service.list_members(db, org_id)
    return [{"user_id": m.user_id, "role": m.role} for m in members]


@router.post("/{org_id}/invites", response_model=OrgInviteRead)
def create_invite_endpoint(
    org_id: str,
    data: OrgInviteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        invite = org_service.create_invite(
            db, current_user, org_id, data.email, data.role
        )
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not allowed")
    return OrgInviteRead(token=invite.token, email=invite.email, role=invite.role)
