from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.services.cache_headers import compute_etag

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_cache.db"
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


def test_etag_header():
    resp = client.get("/healthz")
    body = resp.content
    etag = compute_etag(body)
    resp2 = client.get("/healthz", headers={"If-None-Match": etag})
    assert resp2.status_code == 304
