import asyncio

from app.jobs.queue import update_job_status
from app.services.notifications import send_email


def send_email_job(job_id: str, to: str, subject: str, body: str) -> None:
    update_job_status(job_id, "started")
    try:
        asyncio.run(send_email(to, subject, body))
        update_job_status(job_id, "finished")
    except Exception as exc:  # pragma: no cover
        update_job_status(job_id, "failed", str(exc))
        raise
