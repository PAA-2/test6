from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.api.deps import get_current_user
from app.core.security import get_password_hash, create_access_token
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_notifications.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def create_user(email: str, password: str) -> User:
    db = TestingSessionLocal()
    user = User(email=email, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def set_current_user(user: User):
    app.dependency_overrides[get_current_user] = lambda: user


def test_notification_on_file_upload_and_ws():
    user = create_user("n1@example.com", "pass")
    set_current_user(user)
    token = create_access_token(str(user.id))

    with client.websocket_connect(f"/notifications/ws?token={token}") as ws:
        resp = client.post(
            "/files/upload",
            files={"file": ("test.pdf", b"content", "application/pdf")},
        )
        assert resp.status_code == 200
        data = ws.receive_json()
        assert data["type"] == "file_uploaded"
        nid = data["id"]

    resp = client.get("/notifications")
    assert resp.status_code == 200
    assert resp.json()[0]["id"] == nid
    resp = client.patch(f"/notifications/{nid}/read")
    assert resp.status_code == 200
    assert resp.json()["read"] is True


def test_email_sending(monkeypatch):
    settings.EMAIL_NOTIFICATIONS_ENABLED = True
    user = create_user("n2@example.com", "pass")
    set_current_user(user)

    sent = {}

    async def fake_send_email(to: str, subject: str, body: str) -> None:
        sent["to"] = to

    monkeypatch.setattr("app.services.notifications.send_email", fake_send_email)

    resp = client.post(
        "/files/upload",
        files={"file": ("test.pdf", b"content", "application/pdf")},
    )
    assert resp.status_code == 200
    assert sent["to"] == "n2@example.com"
    settings.EMAIL_NOTIFICATIONS_ENABLED = False
