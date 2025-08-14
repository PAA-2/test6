from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_user_by_id
from app.core.config import settings
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationRead
from app.services.notifications import list_notifications, mark_read, mark_all_read
from app.ws.connection_manager import manager

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=List[NotificationRead])
async def get_notifications(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    page_size: int = 10,
) -> List[Notification]:
    skip = (page - 1) * page_size
    return list_notifications(db, current_user, skip, page_size)


@router.patch("/{notif_id}/read", response_model=NotificationRead)
async def mark_notification_read(
    notif_id: str,
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Notification:
    notif = mark_read(db, current_user, notif_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Not found")
    return notif


@router.patch("/read-all", status_code=204)
async def mark_all_notifications(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    mark_all_read(db, current_user)
    return None


@router.websocket("/ws")
async def notifications_ws(
    websocket: WebSocket, token: str, db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
    except JWTError:
        await websocket.close(code=1008)
        return
    user = get_user_by_id(db, user_id)
    if not user:
        await websocket.close(code=1008)
        return
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
