from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ...database import get_db
from ...models.user import User
from ...services.password_reset import create_reset_token, verify_reset_token
from ...services.notifications import send_email
from ...core.security import get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


class ForgotRequest(BaseModel):
    email: EmailStr


@router.post("/forgot")
async def forgot_password(data: ForgotRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        token = create_reset_token(str(user.id))
        await send_email(
            to=user.email,
            subject="Password reset",
            body=f"Reset token: {token}",
        )
    return {"status": "ok"}


class ResetRequest(BaseModel):
    token: str
    password: str


@router.post("/reset")
async def reset_password(data: ResetRequest, db: Session = Depends(get_db)):
    user_id = verify_reset_token(data.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="invalid token")
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="invalid token")
    user.hashed_password = get_password_hash(data.password)
    db.commit()
    return {"status": "ok"}
