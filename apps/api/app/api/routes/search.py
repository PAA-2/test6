from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.search import (
    FacetsResponse,
    SavedSearchCreate,
    SavedSearchList,
    SavedSearchOut,
    SearchQuery,
    SearchResponse,
    SuggestionItem,
)
from app.services import search as search_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search_endpoint(
    params: SearchQuery = Depends(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = search_service.search(db, current_user, params)
    return SearchResponse(
        items=items, page=params.page, page_size=params.page_size, total=total
    )


@router.get("/facets", response_model=FacetsResponse)
def facets_endpoint(
    params: SearchQuery = Depends(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return search_service.facets(db, current_user, params)


@router.get("/suggestions", response_model=list[SuggestionItem])
def suggestions_endpoint(
    q: str,
    type: str = Query("all"),
    limit: int = Query(8, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return search_service.suggestions(db, current_user, q, type, limit)


@router.post("/saved", response_model=SavedSearchOut)
def save_search_endpoint(
    data: SavedSearchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ss = search_service.create_saved_search(db, current_user, data)
    return SavedSearchOut(
        id=ss.id, name=ss.name, params=ss.params, created_at=ss.created_at
    )


@router.get("/saved", response_model=SavedSearchList)
def list_saved_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = search_service.list_saved_searches(db, current_user, page, page_size)
    return SavedSearchList(
        items=[
            SavedSearchOut(
                id=i.id, name=i.name, params=i.params, created_at=i.created_at
            )
            for i in items
        ],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.delete("/saved/{sid}", status_code=204)
def delete_saved_endpoint(
    sid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ok = search_service.delete_saved_search(db, current_user, sid)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
