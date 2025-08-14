from __future__ import annotations
import os

os.environ["TESTING"] = "1"
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.org_membership import OrgMembership
from app.services.orgs import create_default_org_for_user
from app.api.deps import get_current_user
from app.core.security import get_password_hash
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_limits.db"
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


def create_user(email: str) -> User:
    db = TestingSessionLocal()
    user = User(email=email, hashed_password=get_password_hash("pass"), role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    create_default_org_for_user(db, user)
    db.refresh(user)
    db.expunge(user)
    db.close()
    return user


def set_current_user(user: User):
    app.dependency_overrides[get_current_user] = lambda: user


def test_rate_limit_exceeded():
    os.environ["TESTING"] = "1"
    user = create_user("admin2@example.com")
    set_current_user(user)
    db = TestingSessionLocal()
    org_id = db.query(OrgMembership.org_id).filter_by(user_id=user.id).first()[0]
    db.close()
    resp = client.post(
        f"/orgs/{org_id}/api-keys", json={"name": "key", "scopes": ["projects:read"]}
    )
    key = resp.json()["key"]
    settings.API_RATE_LIMIT_PER_MINUTE = 2
    for i in range(3):
        resp = client.get(
            "/api/v1/projects", headers={"Authorization": f"Bearer {key}"}
        )
    assert resp.status_code == 429
