from datetime import timedelta, datetime, timezone

from passlib.context import CryptContext
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from src.config import settings
from src.exceptions import LoginException, DataConflictException
from src.schemas.users_schemas import UserRequestAdd, UserAdd, UserRequestLogin
from src.services.base_service import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def decode_token(token: str) -> dict | None:
        if token is None:
            return None
        try:
            res = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except (ExpiredSignatureError, DecodeError) as e:
            raise LoginException(detail=f"{e.__class__.__name__}: {e}")
        return res

    async def register_user(self, user_data: UserRequestAdd):
        hashed_pass = self.hash_password(user_data.password)
        new_user = UserAdd(
            email=user_data.email, hashed_password=hashed_pass, nickname=user_data.nickname
        )
        try:
            await self.db.users.add(new_user)
        except DataConflictException as e:
            raise LoginException from e
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
