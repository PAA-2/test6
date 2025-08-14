from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email_notifications: bool | None = None


class UserRead(UserBase):
    id: int
    role: str
    email_notifications: bool

    class Config:
        orm_mode = True


class UserRoleUpdate(BaseModel):
    role: str
