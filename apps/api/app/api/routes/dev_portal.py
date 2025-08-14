from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.org_membership import OrgMembership
from app.models.webhook_delivery import WebhookDelivery
from app.services import api_keys, webhooks

router = APIRouter(prefix="/orgs/{org_id}")


def ensure_admin(db: Session, user_id: int, org_id: str) -> None:
    membership = (
        db.query(OrgMembership)
        .filter(OrgMembership.user_id == user_id, OrgMembership.org_id == org_id)
        .first()
    )
    if not membership or membership.role not in ("owner", "admin"):
        raise PermissionError


@router.post("/api-keys")
def create_api_key(
    org_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    scopes = payload.get("scopes", [])
    name = payload.get("name", "")
    key, key_plain = api_keys.create_api_key(db, org_id, name, scopes)
    return {"id": key.id, "key": key_plain, "name": key.name, "scopes": key.scopes}


@router.get("/api-keys")
def list_api_keys(
    org_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    keys = api_keys.list_api_keys(db, org_id)
    return [
        {
            "id": k.id,
            "name": k.name,
            "prefix": k.prefix,
            "scopes": k.scopes,
            "active": k.active,
        }
        for k in keys
    ]


@router.post("/webhooks")
def create_webhook(
    org_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    endpoint, secret = webhooks.create_endpoint(
        db, org_id, payload.get("url"), payload.get("events", []), payload.get("secret")
    )
    return {
        "id": endpoint.id,
        "secret": secret,
        "url": endpoint.url,
        "events": endpoint.events,
    }


@router.get("/webhooks")
def list_webhooks(
    org_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    endpoints = webhooks.list_endpoints(db, org_id)
    return [
        {"id": e.id, "url": e.url, "events": e.events, "active": e.active}
        for e in endpoints
    ]


@router.get("/webhooks/{endpoint_id}/deliveries")
def list_deliveries(
    org_id: str,
    endpoint_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    deliveries = (
        db.query(WebhookDelivery)
        .filter(WebhookDelivery.endpoint_id == endpoint_id)
        .order_by(WebhookDelivery.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "event": d.event,
            "status": d.status,
            "response_code": d.response_code,
            "attempts": d.attempts,
        }
        for d in deliveries
    ]


@router.post("/webhooks/{endpoint_id}/test")
def send_test(
    org_id: str,
    endpoint_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    data = {"test": True}
    webhooks.queue_event(db, org_id, "test.event", data)
    return Response(status_code=202)
