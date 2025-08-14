from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.api.deps import get_current_user
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_search_saved.db"
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


def create_user(email: str, role: str) -> User:
    db = TestingSessionLocal()
    user = User(email=email, hashed_password=get_password_hash("pass"), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def set_current_user(user: User):
    app.dependency_overrides[get_current_user] = lambda: user


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_saved_search_crud():
    user = create_user("u4@example.com", "admin")
    set_current_user(user)
    app.dependency_overrides[get_db] = override_get_db
    resp = client.post(
        "/search/saved",
        json={"name": "mine", "params": {"q": "x"}},
    )
    assert resp.status_code == 200
    sid = resp.json()["id"]
    resp = client.get("/search/saved")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
    resp = client.delete(f"/search/saved/{sid}")
    assert resp.status_code == 204
