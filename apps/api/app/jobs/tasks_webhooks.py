from __future__ import annotations

import json
from datetime import datetime, timedelta

import httpx

from app.database import SessionLocal
from app.models.webhook_delivery import WebhookDelivery
from app.models.webhook_endpoint import WebhookEndpoint
from app.services.webhooks import generate_signature
from app.jobs.queue import update_job_status
from app.core.config import settings


def deliver_webhook(job_id: str, delivery_id: str) -> None:
    db = SessionLocal()
    delivery = (
        db.query(WebhookDelivery).filter(WebhookDelivery.id == delivery_id).first()
    )
    if not delivery:
        update_job_status(job_id, "failed", "delivery not found")
        db.close()
        return
    endpoint = (
        db.query(WebhookEndpoint)
        .filter(WebhookEndpoint.id == delivery.endpoint_id)
        .first()
    )
    if not endpoint:
        update_job_status(job_id, "failed", "endpoint missing")
        db.close()
        return
    payload = json.dumps(delivery.payload)
    ts = str(int(datetime.utcnow().timestamp()))
    sig = generate_signature(endpoint.secret, ts, payload)
    headers = {
        "X-PAA-Timestamp": ts,
        "X-PAA-Signature": f"t={ts}, v1={sig}",
        "Content-Type": "application/json",
    }
    try:
        update_job_status(job_id, "started")
        resp = httpx.post(
            endpoint.url,
            data=payload,
            headers=headers,
            timeout=settings.WEBHOOK_TIMEOUT_SECONDS,
        )
    except Exception as e:  # pragma: no cover
        delivery.attempts += 1
        if delivery.attempts >= settings.WEBHOOK_MAX_RETRIES:
            delivery.status = "failed"
        else:
            delivery.status = "pending"
            delivery.next_retry_at = datetime.utcnow() + timedelta(
                seconds=2**delivery.attempts
            )
        update_job_status(job_id, "failed", str(e))
    else:
        delivery.attempts += 1
        delivery.response_code = resp.status_code
        if 200 <= resp.status_code < 300:
            delivery.status = "sent"
            update_job_status(job_id, "finished")
        else:
            if delivery.attempts >= settings.WEBHOOK_MAX_RETRIES:
                delivery.status = "failed"
            else:
                delivery.status = "pending"
                delivery.next_retry_at = datetime.utcnow() + timedelta(
                    seconds=2**delivery.attempts
                )
            update_job_status(job_id, "failed", "bad status")
    db.add(delivery)
    db.commit()
    db.close()
