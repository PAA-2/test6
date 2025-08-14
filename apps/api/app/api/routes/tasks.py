from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db, get_current_user, require_role
from app.jobs import queue, tasks_analytics, tasks_files
from app.models.file import File
from app.models.job import Job
from app.schemas.job import JobEnqueueResponse, JobList, JobStatus
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/analytics/rebuild", response_model=JobEnqueueResponse)
def rebuild_analytics(
    scope: str = "global",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> JobEnqueueResponse:
    user_id = current_user.id if scope == "user" else None
    task_id = queue.enqueue(
        "analytics.rebuild",
        tasks_analytics.rebuild_analytics_cache,
        scope,
        user_id,
        owner_id=current_user.id,
    )
    return JobEnqueueResponse(task_id=task_id)


@router.post("/files/{file_id}/thumbnail", response_model=JobEnqueueResponse)
def generate_thumbnail(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobEnqueueResponse:
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if current_user.role != "admin" and file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted")
    task_id = queue.enqueue(
        "thumbnail",
        tasks_files.generate_thumbnail,
        file_id,
        owner_id=current_user.id,
    )
    return JobEnqueueResponse(task_id=task_id)


@router.get("/{task_id}/status", response_model=JobStatus)
def get_status(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobStatus:
    job = db.query(Job).filter(Job.id == task_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user.role != "admin" and job.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted")
    return job


@router.get("/", response_model=JobList)
def list_jobs(
    job_type: Optional[str] = Query(None, alias="type"),
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> JobList:
    query = db.query(Job)
    if job_type:
        query = query.filter(Job.type == job_type)
    if status:
        query = query.filter(Job.status == status)
    total = query.count()
    items = (
        query.order_by(Job.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return JobList(items=items, page=page, page_size=page_size, total=total)
