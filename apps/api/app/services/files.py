from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import File


def save_file(
    db: Session, *, upload: UploadFile, content: bytes, user_id: int, org_id: str
) -> File:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(upload.filename).suffix
    stored_name = f"{uuid4()}{ext}"
    path = upload_dir / stored_name
    with open(path, "wb") as f:
        f.write(content)
    db_file = File(
        owner_id=user_id,
        org_id=org_id,
        original_name=upload.filename,
        stored_name=stored_name,
        mime_type=upload.content_type or "application/octet-stream",
        size_bytes=len(content),
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, *, file: File) -> None:
    upload_dir = Path(settings.UPLOAD_DIR)
    path = upload_dir / file.stored_name
    if path.exists():
        path.unlink()
    db.delete(file)
    db.commit()
