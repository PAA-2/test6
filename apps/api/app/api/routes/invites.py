from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.orgs import OrgInviteRead
from app.services import orgs as org_service

router = APIRouter(prefix="/invites", tags=["orgs"])


@router.get("/{token}", response_model=OrgInviteRead)
def get_invite(token: str, db: Session = Depends(get_db)):
    invite = org_service.get_invite(db, token)
    if not invite or invite.accepted_at or invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Invalid invite")
    return OrgInviteRead(token=invite.token, email=invite.email, role=invite.role)


@router.post("/{token}/accept")
def accept_invite(
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = org_service.accept_invite(db, current_user, token)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid invite")
    return {"accepted": True}
