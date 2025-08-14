from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.orgs import OrgSelect
from app.services import orgs as org_service

router = APIRouter(tags=["orgs"])


@router.post("/me/org")
def set_current_org(
    data: OrgSelect,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        org_service.set_current_org(db, current_user, data.org_id)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not a member of org")
    return {"org_id": data.org_id}
