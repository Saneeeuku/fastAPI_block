from datetime import timedelta, datetime, timezone

from bcrypt import hashpw, checkpw, gensalt
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from src.config import settings
from src.exceptions import (
    TokenException,
    DataConflictException,
    UserConflictException,
    LoginException,
)
from src.schemas.users_schemas import UserRequestAdd, UserAdd, UserRequestLogin
from src.services.base_service import BaseService


class AuthService(BaseService):
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str):
        bytes_pw = password.encode()
        return hashpw(bytes_pw, gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        bytes_pw = plain_password.encode()
        bytes_hpw = hashed_password.encode()
        return checkpw(bytes_pw, bytes_hpw)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        if token is None:
            return None
        try:
            res = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except (ExpiredSignatureError, DecodeError) as e:
            raise TokenException from e
        return res

    async def register_user(self, user_data: UserRequestAdd):
        hashed_pass = self.hash_password(user_data.password)
        new_user = UserAdd(
            email=user_data.email, hashed_password=hashed_pass, nickname=user_data.nickname
        )
        try:
            await self.db.users.add(new_user)
        except DataConflictException as e:
            raise UserConflictException from e
        await self.db.commit()

    async def login_user(self, user_data: UserRequestLogin):
        user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise LoginException
        token = AuthService().create_access_token({"id": user.id, "nickname": user.nickname})
        return token

    async def get_me(self, user_id: int):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user
