from __future__ import annotations

import html
import re
from typing import List

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.file import File
from app.models.saved_search import SavedSearch
from app.models.user import User
from app.schemas.search import (
    FacetsResponse,
    SavedSearchCreate,
    SearchItem,
    SearchQuery,
    SuggestionItem,
)

MAX_SAVED_SEARCHES = 50


def _highlight(text: str | None, q: str | None) -> str:
    if not text:
        return ""
    escaped = html.escape(text)
    if not q:
        return escaped[:100]
    pattern = re.compile(re.escape(q), re.IGNORECASE)
    match = pattern.search(escaped)
    if not match:
        return escaped[:100]
    start = max(match.start() - 20, 0)
    end = min(match.end() + 20, len(escaped))
    snippet = escaped[start:end]
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", snippet)


def _apply_project_filters(query, params: SearchQuery, user: User, org_id: str):
    query = query.filter(Project.org_id == org_id)
    if params.owner == "me" or (user.role != "admin" and params.owner != "all"):
        query = query.filter(Project.owner_id == user.id)
    if params.created_from:
        query = query.filter(Project.created_at >= params.created_from)
    if params.created_to:
        query = query.filter(Project.created_at <= params.created_to)
    if params.status:
        query = query.filter(Project.status.in_(params.status))
    if params.q:
        like = f"%{params.q}%"
        query = query.filter(
            or_(Project.name.ilike(like), Project.description.ilike(like))
        )
    return query


def _apply_file_filters(query, params: SearchQuery, user: User, org_id: str):
    query = query.filter(File.org_id == org_id)
    if params.owner == "me" or (user.role != "admin" and params.owner != "all"):
        query = query.filter(File.owner_id == user.id)
    if params.created_from:
        query = query.filter(File.created_at >= params.created_from)
    if params.created_to:
        query = query.filter(File.created_at <= params.created_to)
    if params.mime:
        query = query.filter(File.mime_type.in_(params.mime))
    if params.q:
        like = f"%{params.q}%"
        query = query.filter(
            or_(File.original_name.ilike(like), File.mime_type.ilike(like))
        )
    return query


def search(db: Session, user: User, params: SearchQuery, org_id: str):
    items: List[SearchItem] = []
    if params.type in ("project", "all"):
        pq = _apply_project_filters(db.query(Project), params, user, org_id)
        for p in pq.all():
            score = (
                1.0
                if params.q
                and params.q.lower() in (p.name + " " + (p.description or "")).lower()
                else 0.0
            )
            snippet = _highlight(p.description or p.name, params.q)
            items.append(
                SearchItem(
                    entity="project",
                    id=p.id,
                    score=score,
                    title=p.name,
                    snippet=snippet,
                    status=p.status,
                    mime=None,
                    owner_id=p.owner_id,
                    created_at=p.created_at,
                )
            )
    if params.type in ("file", "all"):
        fq = _apply_file_filters(db.query(File), params, user, org_id)
        for f in fq.all():
            score = (
                1.0 if params.q and params.q.lower() in f.original_name.lower() else 0.0
            )
            snippet = _highlight(f.original_name, params.q)
            items.append(
                SearchItem(
                    entity="file",
                    id=f.id,
                    score=score,
                    title=f.original_name,
                    snippet=snippet,
                    status=None,
                    mime=f.mime_type,
                    owner_id=f.owner_id,
                    created_at=f.created_at,
                )
            )
    reverse = params.order == "desc"
    if params.sort == "name":
        items.sort(key=lambda x: x.title.lower(), reverse=reverse)
    elif params.sort == "created_at":
        items.sort(key=lambda x: x.created_at, reverse=reverse)
    else:  # score
        items.sort(key=lambda x: x.score, reverse=reverse)
    total = len(items)
    start = (params.page - 1) * params.page_size
    end = start + params.page_size
    return items[start:end], total


def facets(db: Session, user: User, params: SearchQuery, org_id: str) -> FacetsResponse:
    pq = _apply_project_filters(db.query(Project), params, user, org_id)
    sub_p = pq.subquery()
    project_counts = {
        status: count
        for status, count in db.query(sub_p.c.status, func.count())
        .group_by(sub_p.c.status)
        .all()
    }
    fq = _apply_file_filters(db.query(File), params, user, org_id)
    sub_f = fq.subquery()
    mime_counts = [
        {"mime": mime, "count": count}
        for mime, count in db.query(sub_f.c.mime_type, func.count())
        .group_by(sub_f.c.mime_type)
        .all()
    ]
    return FacetsResponse(projects_by_status=project_counts, files_by_mime=mime_counts)


def suggestions(db: Session, user: User, q: str, type_: str, limit: int, org_id: str):
    results: List[SuggestionItem] = []
    if type_ in ("project", "all"):
        query = db.query(Project).filter(
            Project.name.ilike(f"%{q}%"), Project.org_id == org_id
        )
        if user.role != "admin":
            query = query.filter(Project.owner_id == user.id)
        for p in query.limit(limit).all():
            results.append(SuggestionItem(entity="project", title=p.name))
    if len(results) < limit and type_ in ("file", "all"):
        query = db.query(File).filter(
            File.original_name.ilike(f"%{q}%"), File.org_id == org_id
        )
        if user.role != "admin":
            query = query.filter(File.owner_id == user.id)
        for f in query.limit(limit - len(results)).all():
            results.append(SuggestionItem(entity="file", title=f.original_name))
    return results


def create_saved_search(db: Session, user: User, data: SavedSearchCreate):
    count = db.query(SavedSearch).filter(SavedSearch.user_id == user.id).count()
    if count >= MAX_SAVED_SEARCHES:
        raise ValueError("quota exceeded")
    ss = SavedSearch(user_id=user.id, name=data.name, params=data.params)
    db.add(ss)
    db.commit()
    db.refresh(ss)
    return ss


def list_saved_searches(db: Session, user: User, page: int = 1, page_size: int = 10):
    query = (
        db.query(SavedSearch)
        .filter(SavedSearch.user_id == user.id)
        .order_by(SavedSearch.created_at.desc())
    )
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def delete_saved_search(db: Session, user: User, sid: str) -> bool:
    ss = (
        db.query(SavedSearch)
        .filter(SavedSearch.id == sid, SavedSearch.user_id == user.id)
        .first()
    )
    if not ss:
        return False
    db.delete(ss)
    db.commit()
    return True
