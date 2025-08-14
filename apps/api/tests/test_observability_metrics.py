from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_metrics_endpoint():
    client.get("/healthz")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"http_requests_total" in resp.content
