from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.api.deps import get_current_user
from app.core.security import get_password_hash
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_files.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


settings.UPLOAD_DIR = "test_uploads"
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def create_user(email: str, password: str, role: str) -> int:
    db = TestingSessionLocal()
    user = User(email=email, hashed_password=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    uid = user.id
    db.close()
    return uid


def set_current_user(user: User):
    app.dependency_overrides[get_current_user] = lambda: user


def test_upload_and_download_file():
    uid = create_user("u1@example.com", "pass", "viewer")
    user = TestingSessionLocal().query(User).get(uid)
    set_current_user(user)
    resp = client.post(
        "/files/upload",
        files={"file": ("test.pdf", b"content", "application/pdf")},
    )
    assert resp.status_code == 200
    fid = resp.json()["id"]
    resp = client.get(f"/files/{fid}/download")
    assert resp.status_code == 200
    assert resp.content == b"content"
    resp = client.get("/files")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    resp = client.delete(f"/files/{fid}")
    assert resp.status_code == 204
    resp = client.get("/files")
    assert resp.json() == []


def test_upload_invalid_type():
    uid = create_user("u2@example.com", "pass", "viewer")
    user = TestingSessionLocal().query(User).get(uid)
    set_current_user(user)
    resp = client.post(
        "/files/upload",
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert resp.status_code == 400


def test_upload_too_large():
    uid = create_user("u3@example.com", "pass", "viewer")
    user = TestingSessionLocal().query(User).get(uid)
    set_current_user(user)
    settings.MAX_FILE_SIZE_MB = 1
    big_content = b"a" * (2 * 1024 * 1024)
    resp = client.post(
        "/files/upload",
        files={"file": ("big.pdf", big_content, "application/pdf")},
    )
    assert resp.status_code == 400
    settings.MAX_FILE_SIZE_MB = 10
