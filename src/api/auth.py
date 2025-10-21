from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users_schemas import UserRequestAdd, UserAdd, UserRequestLogin
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/registration", summary="Регистрация пользователя")
async def register_user(
    db: DBDep,
    user_data: UserRequestAdd = Body(openapi_examples={
        "1": {
        "summary": "Пользователь 1",
        "value": {
            "email": "qwerty@loop.com",
            "password": "verystrongpassword",
            "nickname": "coolnickname"
            }
            },
        })
):
    hashed_pass = AuthService().hash_password(user_data.password)
    new_user = UserAdd(email=user_data.email, hashed_password=hashed_pass, nickname=user_data.nickname)
    await db.users.add(new_user)
    await db.commit()
    return {"status": "OK"}


@router.post("/login", summary="Авторизация пользователя")
async def login_user(
    db: DBDep,
    response: Response,
    user_data: UserRequestLogin = Body(openapi_examples={
        "1": {
        "summary": "Пользователь 1",
        "value": {
            "email": "qwerty@loop.com",
            "password": "verystrongpassword",
            }
            },
        })
):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    if not AuthService().verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    token = AuthService().create_access_token({"id": user.id, "nickname": user.nickname})
    response.set_cookie("access_token", token)
    return {"access_token": token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.delete("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
