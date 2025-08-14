from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.webhooks import queue_event


def project_created(db: Session, org_id: str, project_id: str) -> None:
    queue_event(db, org_id, "project.created", {"project": {"id": project_id}})


def project_updated(db: Session, org_id: str, project_id: str) -> None:
    queue_event(db, org_id, "project.updated", {"project": {"id": project_id}})


def file_uploaded(db: Session, org_id: str, file_id: str) -> None:
    queue_event(db, org_id, "file.uploaded", {"file": {"id": file_id}})
