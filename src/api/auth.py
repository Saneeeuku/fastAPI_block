from fastapi import APIRouter, Body

from passlib.context import CryptContext


from src.repos.users_repo import UsersRepository
from src.database import async_new_session
from src.schemas.users_schemas import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/registration", summary="Регистрация пользователя")
async def register_user(user_data: UserRequestAdd = Body(openapi_examples={
        "1": {
        "summary": "Пользователь 1",
        "value": {
            "email": "qwerty@loop.com",
            "password": "verystrongpassword",
            "nickname": "coolnickname"
            }
            },
        })):
    async with async_new_session() as session:
        hashed_pass = pwd_context.hash(user_data.password)
        new_user = UserAdd(email=user_data.email, hashed_password=hashed_pass, nickname=user_data.nickname)
        await UsersRepository(session).add(new_user)
        await session.commit()
    return {"status": "OK"}
