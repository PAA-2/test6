from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"
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


def get_client() -> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_register_login_me():
    client = get_client()
    resp = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secret", "full_name": "Test"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()

    resp = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "secret"},
    )
    assert resp.status_code == 200
    tokens = resp.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    resp = client.get("/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"

    resp = client.put("/me", json={"full_name": "Updated"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Updated"
