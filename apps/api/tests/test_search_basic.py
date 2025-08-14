from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.project import Project
from app.models.file import File
from app.models.org_membership import OrgMembership
from app.services.orgs import create_default_org_for_user
from app.api.deps import get_current_user
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_search.db"
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
    create_default_org_for_user(db, user)
    db.refresh(user)
    db.expunge(user)
    db.close()
    return user


def set_current_user(user: User):
    app.dependency_overrides[get_current_user] = lambda: user


def setup_data() -> User:
    user = create_user("u@example.com", "admin")
    db = TestingSessionLocal()
    org_id = (
        db.query(OrgMembership.org_id)
        .filter(OrgMembership.user_id == user.id)
        .first()[0]
    )
    p = Project(
        name="Contract Project",
        description="something contract",
        status="active",
        owner_id=user.id,
        org_id=org_id,
    )
    f = File(
        original_name="contract.pdf",
        stored_name="x",
        mime_type="application/pdf",
        size_bytes=1,
        owner_id=user.id,
        org_id=org_id,
    )
    db.add_all([p, f])
    db.commit()
    db.close()
    return user


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_search_projects_and_files():
    user = setup_data()
    set_current_user(user)
    app.dependency_overrides[get_db] = override_get_db
    resp = client.get("/search", params={"q": "contract", "type": "all"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    titles = [i["title"] for i in data["items"]]
    assert "Contract Project" in titles
    assert "contract.pdf" in titles
