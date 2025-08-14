from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_role
from app.core.config import settings
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)
from app.services.projects import create_project, delete_project, update_project

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead)
def create_project_endpoint(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "editor")),
) -> Project:
    return create_project(
        db, project_in=project_in.model_dump(), user_id=current_user.id
    )


@router.get("", response_model=List[ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    q: Optional[str] = None,
    sort: str = Query("created_at", pattern="^(created_at|name|status)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = 1,
    page_size: int = settings.PROJECTS_PAGE_SIZE_DEFAULT,
) -> List[Project]:
    query = db.query(Project)
    if q:
        like = f"%{q}%"
        query = query.filter(Project.name.ilike(like) | Project.description.ilike(like))
    if order == "asc":
        query = query.order_by(getattr(Project, sort).asc())
    else:
        query = query.order_by(getattr(Project, sort).desc())
    page_size = min(page_size, settings.PROJECTS_PAGE_SIZE_MAX)
    return query.offset((page - 1) * page_size).limit(page_size).all()


@router.get("/{project_id}", response_model=ProjectRead)
def read_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project_endpoint(
    project_id: str,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "editor")),
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return update_project(
        db,
        project=project,
        data=project_in.model_dump(exclude_unset=True),
        user_id=current_user.id,
    )


@router.delete("/{project_id}", status_code=204)
def delete_project_endpoint(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "editor")),
) -> None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role == "editor" and (
        project.owner_id != current_user.id or not settings.ALLOW_OWNER_DELETE
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    if current_user.role == "admin" or project.owner_id == current_user.id:
        delete_project(db, project=project, user_id=current_user.id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
