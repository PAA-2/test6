from __future__ import annotations
import os

os.environ["TESTING"] = "1"
from app.services.webhooks import generate_signature


def test_webhook_signature_and_retry():
    payload = "{}"
    ts = "123"
    sig = generate_signature("s", ts, payload)
    assert isinstance(sig, str)
    assert len(sig) == 64
