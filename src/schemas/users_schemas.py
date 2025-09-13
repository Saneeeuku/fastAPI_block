from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    nickname: str


class User(BaseModel):
    id: int
    email: EmailStr
    nickname: str


class UserWithHashedPassword(User):
    hashed_password: str


class UserRequestLogin(BaseModel):
    email: EmailStr
    password: str
