from __future__ import annotations

from datetime import datetime, timedelta
import uuid
from typing import List

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.organization import Organization
from app.models.org_membership import OrgMembership
from app.models.org_invite import OrgInvite
from app.models.user import User


INVITE_TTL = getattr(settings, "INVITE_TOKEN_TTL_HOURS", 72)


def create_default_org_for_user(db: Session, user: User) -> str:
    org = Organization(name=f"{user.email} Org", slug=f"default-{user.id}")
    db.add(org)
    db.flush()
    membership = OrgMembership(org_id=org.id, user_id=user.id, role="owner")
    user.last_selected_org_id = org.id
    db.add(membership)
    db.commit()
    return org.id


def create_org(db: Session, user: User, name: str) -> Organization:
    slug = f"{name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:6]}"
    org = Organization(name=name, slug=slug)
    db.add(org)
    db.flush()
    membership = OrgMembership(org_id=org.id, user_id=user.id, role="owner")
    db.add(membership)
    db.commit()
    return org


def list_orgs(db: Session, user: User) -> List[Organization]:
    org_ids = (
        db.query(OrgMembership.org_id).filter(OrgMembership.user_id == user.id).all()
    )
    ids = [o[0] for o in org_ids]
    if not ids:
        return []
    return db.query(Organization).filter(Organization.id.in_(ids)).all()


def ensure_org_admin(db: Session, user: User, org_id: str) -> None:
    membership = (
        db.query(OrgMembership)
        .filter(OrgMembership.user_id == user.id, OrgMembership.org_id == org_id)
        .first()
    )
    if not membership or membership.role not in ("owner", "admin"):
        raise PermissionError


def list_members(db: Session, org_id: str) -> List[OrgMembership]:
    return db.query(OrgMembership).filter(OrgMembership.org_id == org_id).all()


def create_invite(
    db: Session, user: User, org_id: str, email: str, role: str
) -> OrgInvite:
    ensure_org_admin(db, user, org_id)
    token = str(uuid.uuid4())
    invite = OrgInvite(
        org_id=org_id,
        email=email,
        role=role,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=INVITE_TTL),
        created_by=user.id,
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite


def get_invite(db: Session, token: str) -> OrgInvite | None:
    return db.query(OrgInvite).filter(OrgInvite.token == token).first()


def accept_invite(db: Session, user: User, token: str) -> bool:
    invite = get_invite(db, token)
    if not invite or invite.accepted_at or invite.expires_at < datetime.utcnow():
        return False
    membership = OrgMembership(org_id=invite.org_id, user_id=user.id, role=invite.role)
    invite.accepted_at = datetime.utcnow()
    db.add(membership)
    db.add(invite)
    db.commit()
    return True


def set_current_org(db: Session, user: User, org_id: str) -> None:
    membership = (
        db.query(OrgMembership)
        .filter(OrgMembership.user_id == user.id, OrgMembership.org_id == org_id)
        .first()
    )
    if not membership:
        raise PermissionError
    user.last_selected_org_id = org_id
    db.add(user)
    db.commit()
