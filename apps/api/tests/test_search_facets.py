from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.project import Project
from app.models.file import File
from app.api.deps import get_current_user
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_search_facets.db"
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


def setup_data() -> User:
    user = create_user("u2@example.com", "admin")
    db = TestingSessionLocal()
    p1 = Project(name="A", description="", status="draft", owner_id=user.id)
    p2 = Project(name="B", description="", status="active", owner_id=user.id)
    f1 = File(
        original_name="file1.pdf",
        stored_name="f1",
        mime_type="application/pdf",
        size_bytes=1,
        owner_id=user.id,
    )
    f2 = File(
        original_name="img.png",
        stored_name="f2",
        mime_type="image/png",
        size_bytes=1,
        owner_id=user.id,
    )
    db.add_all([p1, p2, f1, f2])
    db.commit()
    db.close()
    return user


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_facets_counts():
    user = setup_data()
    set_current_user(user)
    app.dependency_overrides[get_db] = override_get_db
    resp = client.get("/search/facets", params={"type": "all"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["projects_by_status"]["draft"] == 1
    assert any(
        f["mime"] == "application/pdf" and f["count"] == 1
        for f in data["files_by_mime"]
    )
