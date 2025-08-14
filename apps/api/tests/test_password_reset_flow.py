from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_reset.db"
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


def test_password_reset_flow():
    client.post(
        "/auth/register",
        json={"email": "a@example.com", "password": "oldpass", "full_name": "A"},
    )
    from app.services.password_reset import create_reset_token

    token = create_reset_token("1")
    client.post("/auth/reset", json={"token": token, "password": "newpass"})
    resp = client.post(
        "/auth/login", data={"username": "a@example.com", "password": "newpass"}
    )
    assert resp.status_code == 200
