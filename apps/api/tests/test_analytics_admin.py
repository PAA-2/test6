from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.api.deps import get_current_user
from app.core.security import get_password_hash
from app.services.analytics import clear_cache

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_analytics_admin.db"
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


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_top_users_admin_only():
    admin = create_user("a3@example.com", "admin")
    app.dependency_overrides[get_current_user] = lambda: admin
    clear_cache()
    resp = client.get("/analytics/top-users")
    assert resp.status_code == 200
    app.dependency_overrides.pop(get_current_user, None)

    editor = create_user("u1@example.com", "editor")
    app.dependency_overrides[get_current_user] = lambda: editor
    resp = client.get("/analytics/top-users")
    assert resp.status_code == 403
    app.dependency_overrides.pop(get_current_user, None)
