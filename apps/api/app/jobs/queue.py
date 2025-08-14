from __future__ import annotations

import os
from datetime import datetime
from uuid import uuid4
from typing import Any

from redis import Redis
from rq import Queue, Retry

from app.core.config import settings
from app.database import SessionLocal
from app.models.job import Job

if os.getenv("TESTING"):
    import fakeredis

    redis_conn: Redis = fakeredis.FakeRedis()
else:
    redis_conn = Redis.from_url(settings.REDIS_URL)

queue = Queue("default", connection=redis_conn)


def enqueue(job_type: str, func: Any, *args: Any, owner_id: int | None = None) -> str:
    db = SessionLocal()
    job_id = str(uuid4())
    job = Job(
        id=job_id, type=job_type, args=list(args), status="queued", owner_id=owner_id
    )
    db.add(job)
    db.commit()
    retry = Retry(
        max=settings.JOBS_MAX_RETRIES, interval=[0] * settings.JOBS_MAX_RETRIES
    )
    queue.enqueue(func, job_id, *args, retry=retry)
    db.close()
    return job_id


def update_job_status(job_id: str, status: str, error_text: str | None = None) -> None:
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = status
        if status == "started":
            job.started_at = datetime.utcnow()
        if status in {"finished", "failed"}:
            job.finished_at = datetime.utcnow()
        if error_text:
            job.error_text = error_text
        db.add(job)
        db.commit()
    db.close()
