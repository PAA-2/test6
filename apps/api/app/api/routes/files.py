from typing import List
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.file import File as FileModel
from app.models.user import User
from app.schemas.file import FileRead
from app.services.files import delete_file, save_file

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=FileRead)
async def upload_file(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
):
    if file.content_type not in settings.ALLOWED_FILE_TYPES.split(","):
        raise HTTPException(status_code=400, detail="Invalid file type")
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    db_file = save_file(db, upload=file, content=content, user_id=current_user.id)
    return db_file


@router.get("", response_model=List[FileRead])
def list_files(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    page_size: int = 10,
    sort: str = "created_at",
    order: str = "desc",
):
    if page_size > 100:
        page_size = 100
    skip = (page - 1) * page_size
    query = db.query(FileModel)
    if current_user.role != "admin":
        query = query.filter(FileModel.owner_id == current_user.id)
    if sort not in {"created_at", "original_name"}:
        sort = "created_at"
    sort_col = getattr(FileModel, sort)
    if order == "desc":
        sort_col = sort_col.desc()
    files = query.order_by(sort_col).offset(skip).limit(page_size).all()
    return files


@router.get("/{file_id}/download")
def download_file(
    file_id: str,
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(FileModel).get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if current_user.role != "admin" and file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    path = Path(settings.UPLOAD_DIR) / file.stored_name
    if not path.exists():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(path, media_type=file.mime_type, filename=file.original_name)


@router.delete("/{file_id}", status_code=204)
def delete_file_endpoint(
    file_id: str,
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file = db.query(FileModel).get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if current_user.role != "admin" and file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    delete_file(db, file=file)
    return None
