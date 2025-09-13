from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.repos.users_repo import UsersRepository
from src.database import async_new_session
from src.schemas.users_schemas import UserRequestAdd, UserAdd, UserRequestLogin
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


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
        hashed_pass = AuthService().hash_password(user_data.password)
        new_user = UserAdd(email=user_data.email, hashed_password=hashed_pass, nickname=user_data.nickname)
        await UsersRepository(session).add(new_user)
        await session.commit()
    return {"status": "OK"}


@router.post("/login", summary="Авторизация пользователя")
async def register_user(
        response: Response,
        user_data: UserRequestLogin = Body(openapi_examples={
        "1": {
        "summary": "Пользователь 1",
        "value": {
            "email": "qwerty@loop.com",
            "password": "verystrongpassword",
            }
            },
        })):
    async with async_new_session() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        token = AuthService().create_access_token({"id": user.id, "nickname": user.nickname})
        response.set_cookie("access_token", token)
    return {"access_token": token}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_new_session() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
