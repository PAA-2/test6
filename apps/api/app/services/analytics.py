from __future__ import annotations

from datetime import datetime, timedelta
from threading import Lock
from typing import Any, Dict, List
import time

from sqlalchemy import func, cast, Date
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.project import Project
from app.models.file import File
from app.models.notification import Notification
from app.models.user import User

_cache: Dict[str, tuple[float, Any]] = {}
_lock = Lock()
TTL = settings.ANALYTICS_CACHE_TTL_SECONDS


def _get_cache(key: str) -> Any | None:
    with _lock:
        item = _cache.get(key)
        if item and item[0] > time.time():
            return item[1]
    return None


def _set_cache(key: str, value: Any) -> None:
    with _lock:
        _cache[key] = (time.time() + TTL, value)


def clear_cache() -> None:
    with _lock:
        _cache.clear()


def get_summary(db: Session, user: User) -> Dict[str, Any]:
    key = f"summary:{user.id}:{user.role}"
    cached = _get_cache(key)
    if cached:
        return cached

    project_filters = []
    file_filters = []
    if user.role != "admin":
        project_filters.append(Project.owner_id == user.id)
        file_filters.append(File.owner_id == user.id)

    projects_total = (
        db.query(func.count(Project.id)).filter(*project_filters).scalar() or 0
    )
    by_status_rows = (
        db.query(Project.status, func.count(Project.id))
        .filter(*project_filters)
        .group_by(Project.status)
        .all()
    )
    projects_by_status = {status: count for status, count in by_status_rows}

    files_total = db.query(func.count(File.id)).filter(*file_filters).scalar() or 0
    files_bytes_total = (
        db.query(func.coalesce(func.sum(File.size_bytes), 0))
        .filter(*file_filters)
        .scalar()
        or 0
    )
    top_mime_rows = (
        db.query(File.mime_type, func.count(File.id))
        .filter(*file_filters)
        .group_by(File.mime_type)
        .order_by(func.count(File.id).desc())
        .limit(5)
        .all()
    )
    files_top_mime = [{"mime": mime, "count": count} for mime, count in top_mime_rows]

    unread = (
        db.query(func.count(Notification.id))
        .filter(Notification.user_id == user.id, Notification.read.is_(False))
        .scalar()
        or 0
    )

    data = {
        "projects_total": projects_total,
        "projects_by_status": projects_by_status,
        "files_total": files_total,
        "files_bytes_total": files_bytes_total,
        "files_top_mime": files_top_mime,
        "notifications_unread": unread,
    }
    _set_cache(key, data)
    return data


def get_projects_per_day(db: Session, user: User, days: int) -> List[Dict[str, Any]]:
    key = f"ppd:{user.id}:{user.role}:{days}"
    cached = _get_cache(key)
    if cached:
        return cached

    start = datetime.utcnow().date() - timedelta(days=days - 1)
    query = db.query(
        cast(Project.created_at, Date).label("day"),
        func.count(Project.id).label("count"),
    ).filter(cast(Project.created_at, Date) >= start)

    if user.role != "admin":
        query = query.filter(Project.owner_id == user.id)

    rows = query.group_by("day").order_by("day").all()
    result = [{"date": day.isoformat(), "count": count} for day, count in rows]
    _set_cache(key, result)
    return result


def get_top_users(db: Session, limit: int) -> List[Dict[str, Any]]:
    key = f"top:{limit}"
    cached = _get_cache(key)
    if cached:
        return cached

    rows = (
        db.query(User.id, User.email, func.count(Project.id).label("projects_count"))
        .join(Project, Project.owner_id == User.id)
        .group_by(User.id)
        .order_by(func.count(Project.id).desc())
        .limit(limit)
        .all()
    )
    result = [
        {"user_id": uid, "email": email, "projects_count": count}
        for uid, email, count in rows
    ]
    _set_cache(key, result)
    return result
