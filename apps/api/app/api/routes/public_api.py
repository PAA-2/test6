from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps.api_key_auth import ApiKeyContext, api_key_auth
from app.models.project import Project
from app.models.org_membership import OrgMembership
from app.models.file import File
from app.services.projects import create_project

router = APIRouter(prefix="/api/v1")


@router.get("/projects")
def api_projects_list(
    response: Response,
    ctx: ApiKeyContext = Depends(api_key_auth),
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 10,
):
    q = db.query(Project).filter(Project.org_id == ctx.key.org_id)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    response.headers["X-RateLimit-Limit"] = str(ctx.limit)
    response.headers["X-RateLimit-Remaining"] = str(ctx.remaining)
    response.headers["X-RateLimit-Reset"] = str(ctx.reset)
    return {
        "items": [{"id": p.id, "name": p.name, "status": p.status} for p in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/projects/{project_id}")
def api_project_get(
    project_id: str,
    response: Response,
    ctx: ApiKeyContext = Depends(api_key_auth),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.org_id == ctx.key.org_id)
        .first()
    )
    if not project:
        return Response(status_code=404)
    response.headers["X-RateLimit-Limit"] = str(ctx.limit)
    response.headers["X-RateLimit-Remaining"] = str(ctx.remaining)
    response.headers["X-RateLimit-Reset"] = str(ctx.reset)
    return {"id": project.id, "name": project.name, "status": project.status}


@router.post("/projects")
def api_project_create(
    data: dict,
    response: Response,
    ctx: ApiKeyContext = Depends(api_key_auth),
    db: Session = Depends(get_db),
):
    if "projects:write" not in ctx.key.scopes:
        return Response(status_code=403)
    owner = db.query(OrgMembership).filter_by(org_id=ctx.key.org_id).first()
    owner_id = owner.user_id if owner else None
    if owner_id is None:
        return Response(status_code=400)
    project_in = {
        "name": data.get("name"),
        "description": data.get("description"),
        "status": data.get("status", "draft"),
        "org_id": ctx.key.org_id,
    }
    project = create_project(db, project_in=project_in, user_id=owner_id or 0)
    response.headers["X-RateLimit-Limit"] = str(ctx.limit)
    response.headers["X-RateLimit-Remaining"] = str(ctx.remaining)
    response.headers["X-RateLimit-Reset"] = str(ctx.reset)
    return {"id": project.id, "name": project.name, "status": project.status}


@router.get("/files")
def api_files_list(
    response: Response,
    ctx: ApiKeyContext = Depends(api_key_auth),
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 10,
):
    q = db.query(File).filter(File.org_id == ctx.key.org_id)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    response.headers["X-RateLimit-Limit"] = str(ctx.limit)
    response.headers["X-RateLimit-Remaining"] = str(ctx.remaining)
    response.headers["X-RateLimit-Reset"] = str(ctx.reset)
    return {
        "items": [
            {"id": f.id, "original_name": f.original_name, "mime_type": f.mime_type}
            for f in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/files/{file_id}")
def api_file_get(
    file_id: str,
    response: Response,
    ctx: ApiKeyContext = Depends(api_key_auth),
    db: Session = Depends(get_db),
):
    file = (
        db.query(File).filter(File.id == file_id, File.org_id == ctx.key.org_id).first()
    )
    if not file:
        return Response(status_code=404)
    response.headers["X-RateLimit-Limit"] = str(ctx.limit)
    response.headers["X-RateLimit-Remaining"] = str(ctx.remaining)
    response.headers["X-RateLimit-Reset"] = str(ctx.reset)
    return {
        "id": file.id,
        "original_name": file.original_name,
        "mime_type": file.mime_type,
    }
