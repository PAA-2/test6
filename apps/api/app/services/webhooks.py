from __future__ import annotations

import hmac
import hashlib
import secrets
import uuid
from datetime import datetime
from typing import List, Dict

from sqlalchemy.orm import Session

from app.jobs.queue import enqueue
from app.models.webhook_endpoint import WebhookEndpoint
from app.models.webhook_delivery import WebhookDelivery


def create_endpoint(
    db: Session, org_id: str, url: str, events: List[str], secret: str | None = None
) -> tuple[WebhookEndpoint, str]:
    secret = secret or secrets.token_hex(16)
    endpoint = WebhookEndpoint(org_id=org_id, url=url, events=events, secret=secret)
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    return endpoint, secret


def list_endpoints(db: Session, org_id: str) -> List[WebhookEndpoint]:
    return db.query(WebhookEndpoint).filter(WebhookEndpoint.org_id == org_id).all()


def delete_endpoint(db: Session, endpoint: WebhookEndpoint) -> None:
    db.delete(endpoint)
    db.commit()


def queue_event(db: Session, org_id: str, event: str, data: Dict) -> None:
    endpoints = (
        db.query(WebhookEndpoint)
        .filter(WebhookEndpoint.org_id == org_id, WebhookEndpoint.active)
        .all()
    )
    payload = {
        "id": str(uuid.uuid4()),
        "event": event,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }
    from app.jobs.tasks_webhooks import deliver_webhook

    for ep in endpoints:
        delivery = WebhookDelivery(endpoint_id=ep.id, event=event, payload=payload)
        db.add(delivery)
        db.commit()
        enqueue("webhook", deliver_webhook, delivery.id)


def generate_signature(secret: str, timestamp: str, payload: str) -> str:
    base = f"{timestamp}.{payload}"
    return hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest()
