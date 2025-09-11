from pydantic import BaseModel, EmailStr


class _UserBase(BaseModel):
    email: EmailStr
    nickname: str


class UserRequestAdd(_UserBase):
    password: str


class UserAdd(_UserBase):
    hashed_password: str


class User(_UserBase):
    id: int
