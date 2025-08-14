from app.jobs.queue import update_job_status
from app.database import SessionLocal
from app.services import analytics
from app.models.user import User


def rebuild_analytics_cache(
    job_id: str, scope: str, user_id: int | None = None
) -> None:
    db = SessionLocal()
    update_job_status(job_id, "started")
    try:
        analytics.clear_cache()
        if scope == "user" and user_id is not None:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                analytics.get_summary(db, user)
        update_job_status(job_id, "finished")
    except Exception as exc:  # pragma: no cover
        update_job_status(job_id, "failed", str(exc))
        raise
    finally:
        db.close()
