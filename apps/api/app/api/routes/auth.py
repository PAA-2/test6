from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from redis import Redis
import fakeredis

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.core.security_hardening.brute_force_guard import BruteForceGuard
from app.database import get_db
from app.models.user import User
from app.schemas.auth import RefreshToken, Token
from app.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])
try:
    redis_conn = Redis.from_url(settings.REDIS_URL)
    redis_conn.ping()
except Exception:
    redis_conn = fakeredis.FakeRedis()
guard = BruteForceGuard(redis_conn)


@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Token:
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    if not guard.allow(request.client.host, form_data.username):
        raise HTTPException(status_code=429, detail="Too many attempts")
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
def logout() -> dict:
    return {"msg": "Logged out"}


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshToken) -> Token:
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = decoded.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token = create_access_token(str(user_id))
    refresh_token = create_refresh_token(str(user_id))
    return Token(access_token=access_token, refresh_token=refresh_token)
