from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.models.user import User
from app.schemas.analytics import AnalyticsSummary, ProjectPerDay, TopUser
from app.services import analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analytics.get_summary(db, current_user)


@router.get("/projects-per-day", response_model=list[ProjectPerDay])
def projects_per_day(
    days: int = Query(30, ge=7, le=90),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analytics.get_projects_per_day(db, current_user, days)


@router.get(
    "/top-users",
    response_model=list[TopUser],
    dependencies=[Depends(require_role("admin"))],
)
def top_users(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    return analytics.get_top_users(db, limit)
