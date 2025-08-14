from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.api.deps import get_current_user
from app.core.security import get_password_hash
from app.services.orgs import create_default_org_for_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_orgs.db"
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


def test_invite_accept_flow():
    owner = create_user("owner2@example.com")
    set_current_user(owner)
    resp = client.post("/orgs", json={"name": "InviteOrg"})
    org_id = resp.json()["id"]
    resp = client.post(
        f"/orgs/{org_id}/invites",
        json={"email": "user2@example.com", "role": "member"},
    )
    token = resp.json()["token"]
    user2 = create_user("user2@example.com")
    set_current_user(user2)
    resp = client.get(f"/invites/{token}")
    assert resp.status_code == 200
    resp = client.post(f"/invites/{token}/accept")
    assert resp.status_code == 200
    set_current_user(owner)
    resp = client.get(f"/orgs/{org_id}/members")
    ids = [m["user_id"] for m in resp.json()]
    assert user2.id in ids
