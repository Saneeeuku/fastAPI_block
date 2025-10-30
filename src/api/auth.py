from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import LoginException
from src.schemas.users_schemas import UserRequestAdd, UserRequestLogin
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/registration", summary="Регистрация пользователя")
async def register_user(
    db: DBDep,
    user_data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Пользователь 1",
                "value": {
                    "email": "qwerty@loop.com",
                    "password": "verystrongpassword",
                    "nickname": "coolnickname",
                },
            },
        }
    ),
):
    try:
        await AuthService(db).register_user(user_data)
    except LoginException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    return {"status": "OK"}


@router.post("/login", summary="Авторизация пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    user_data: UserRequestLogin = Body(
        openapi_examples={
            "1": {
                "summary": "Пользователь 1",
                "value": {
                    "email": "qwerty@loop.com",
                    "password": "verystrongpassword",
                },
            },
        }
    ),
):
    try:
        token = await AuthService(db).login_user(user_data)
    except LoginException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    response.set_cookie("access_token", token)
    return {"access_token": token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await AuthService(db).get_me(user_id)
    return user


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
