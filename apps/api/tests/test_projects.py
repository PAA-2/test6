from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.api.deps import get_current_user
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_projects.db"
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


def test_viewer_cannot_create_project():
    uid = create_user("viewer@example.com", "pass", "viewer")
    user = TestingSessionLocal().query(User).get(uid)
    set_current_user(user)
    resp = client.post(
        "/projects",
        json={"name": "Proj1", "description": "Desc", "status": "draft"},
    )
    assert resp.status_code == 403


def test_editor_crud_project():
    uid = create_user("editor@example.com", "pass", "editor")
    user = TestingSessionLocal().query(User).get(uid)
    set_current_user(user)
    resp = client.post(
        "/projects",
        json={"name": "Proj2", "description": "Desc", "status": "draft"},
    )
    assert resp.status_code == 200
    project = resp.json()
    pid = project["id"]
    resp = client.put(
        f"/projects/{pid}",
        json={"name": "Proj2-upd"},
    )
    assert resp.status_code == 200
    resp = client.delete(f"/projects/{pid}")
    assert resp.status_code == 204


def test_admin_list_projects():
    uid = create_user("admin@example.com", "pass", "admin")
    user = TestingSessionLocal().query(User).get(uid)
    set_current_user(user)
    resp = client.get("/projects")
    assert resp.status_code == 200
