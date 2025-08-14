from datetime import datetime, timedelta

from app.jobs.queue import update_job_status
from app.database import SessionLocal
from app.core.config import settings
from app.models.notification import Notification


def cleanup_notifications(job_id: str) -> None:
    db = SessionLocal()
    update_job_status(job_id, "started")
    try:
        cutoff = datetime.utcnow() - timedelta(
            days=settings.NOTIFICATIONS_RETENTION_DAYS
        )
        db.query(Notification).filter(
            Notification.read.is_(True), Notification.created_at < cutoff
        ).delete()
        db.commit()
        update_job_status(job_id, "finished")
    except Exception as exc:  # pragma: no cover
        db.rollback()
        update_job_status(job_id, "failed", str(exc))
        raise
    finally:
        db.close()
