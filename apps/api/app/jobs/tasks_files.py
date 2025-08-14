from pathlib import Path
from PIL import Image

from app.jobs.queue import update_job_status
from app.database import SessionLocal
from app.models.file import File
from app.core.config import settings

THUMB_DIR = Path("storage/thumbnails")


def generate_thumbnail(job_id: str, file_id: str) -> None:
    db = SessionLocal()
    update_job_status(job_id, "started")
    try:
        file = db.query(File).filter(File.id == file_id).first()
        if not file:
            raise ValueError("file not found")
        if file.mime_type not in ("image/png", "image/jpeg"):
            raise ValueError("not an image")
        src = Path(settings.UPLOAD_DIR) / file.stored_name
        THUMB_DIR.mkdir(parents=True, exist_ok=True)
        dest = THUMB_DIR / f"{file.id}.jpg"
        with Image.open(src) as img:
            img.thumbnail((settings.THUMBNAIL_MAX_SIZE, settings.THUMBNAIL_MAX_SIZE))
            img.save(dest, quality=settings.THUMBNAIL_QUALITY)
        update_job_status(job_id, "finished")
    except Exception as exc:  # pragma: no cover
        update_job_status(job_id, "failed", str(exc))
        raise
    finally:
        db.close()


def cleanup_orphan_files(job_id: str) -> None:
    db = SessionLocal()
    update_job_status(job_id, "started")
    try:
        existing = {f.stored_name for f in db.query(File).all()}
        upload_dir = Path(settings.UPLOAD_DIR)
        for path in upload_dir.glob("*"):
            if path.name not in existing:
                path.unlink(missing_ok=True)
        update_job_status(job_id, "finished")
    except Exception as exc:  # pragma: no cover
        update_job_status(job_id, "failed", str(exc))
    finally:
        db.close()
