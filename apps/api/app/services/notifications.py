from typing import Any, Dict
import aiosmtplib
from email.message import EmailMessage

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.notification import Notification
from app.models.user import User
from app.ws.connection_manager import manager


async def send_email(to: str, subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = settings.SMTP_USER or "no-reply@example.com"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body, subtype="html")
    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER or None,
        password=settings.SMTP_PASS or None,
    )


async def create_notification(
    db: Session,
    *,
    user: User,
    type: str,
    message: str,
    data: Dict[str, Any] | None = None,
) -> Notification:
    notif = Notification(
        user_id=user.id, type=type, message=message, data=data or {}, read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    await manager.send_personal_message(
        user.id,
        {
            "id": notif.id,
            "type": notif.type,
            "message": notif.message,
            "data": notif.data,
            "read": notif.read,
            "created_at": notif.created_at.isoformat(),
        },
    )
    if settings.EMAIL_NOTIFICATIONS_ENABLED and user.email_notifications:
        await send_email(user.email, f"Notification: {type}", message)
    return notif


def list_notifications(
    db: Session, user: User, skip: int, limit: int
) -> list[Notification]:
    return (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def mark_read(db: Session, user: User, notif_id: str) -> Notification | None:
    notif = (
        db.query(Notification)
        .filter(Notification.id == notif_id, Notification.user_id == user.id)
        .first()
    )
    if notif:
        notif.read = True
        db.add(notif)
        db.commit()
        db.refresh(notif)
    return notif


def mark_all_read(db: Session, user: User) -> None:
    db.query(Notification).filter(
        Notification.user_id == user.id, Notification.read.is_(False)
    ).update({"read": True})
    db.commit()
