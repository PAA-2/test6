from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.feature_flags.services import get_flag, set_flag

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_flags.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def test_toggle_feature_flag():
    db = TestingSessionLocal()
    set_flag(db, "test", True)
    assert get_flag(db, "test") is True
    set_flag(db, "test", False)
    assert get_flag(db, "test") is False
    db.close()
