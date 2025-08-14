from typing import Any, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from .models.audit_log import AuditLog


def log_action(
    db: Session,
    *,
    actor_id: Optional[str],
    org_id: Optional[str],
    action: str,
    target_type: Optional[str] = None,
    target_id: Optional[str] = None,
    success: bool = True,
    details: Optional[dict[str, Any]] = None,
    ip: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> AuditLog:
    entry = AuditLog(
        id=uuid4(),
        actor_id=actor_id,
        org_id=org_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        success=success,
        details=details,
        ip=ip,
        user_agent=user_agent,
    )
    db.add(entry)
    db.commit()
    return entry
