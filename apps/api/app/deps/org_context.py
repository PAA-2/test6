from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.org_membership import OrgMembership
from app.services.orgs import create_default_org_for_user


async def get_current_org_id(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    x_org_id: str | None = Header(default=None, alias="X-Org-Id"),
) -> str:
    org_id = x_org_id or current_user.last_selected_org_id
    membership = None
    if org_id:
        membership = (
            db.query(OrgMembership)
            .filter(
                OrgMembership.user_id == current_user.id, OrgMembership.org_id == org_id
            )
            .first()
        )
    if not membership:
        # ensure user has at least a default org
        existing = (
            db.query(OrgMembership)
            .filter(OrgMembership.user_id == current_user.id)
            .first()
        )
        if not existing:
            org_id = create_default_org_for_user(db, current_user)
            membership = (
                db.query(OrgMembership)
                .filter(
                    OrgMembership.user_id == current_user.id,
                    OrgMembership.org_id == org_id,
                )
                .first()
            )
        else:
            org_id = existing.org_id
            membership = existing
    if current_user.last_selected_org_id != org_id:
        current_user.last_selected_org_id = org_id
        db.merge(current_user)
        db.commit()
    return org_id
