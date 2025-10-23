from typing import Annotated

from pydantic import BaseModel
from fastapi import Query, Depends, Request, HTTPException

from src.services.auth_service import AuthService
from src.utils.db_manager import DBManager
from src.database import async_new_session


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gt=0)]
    per_page: Annotated[int | None, Query(5, gt=0, le=30)]


class TokenDecodeParams(BaseModel):
    id: int
    nickname: str


class RoomsParams(BaseModel):
    title: Annotated[str | None, Query(None)]
    description: Annotated[str | None, Query(None)]
    price: Annotated[int | None, Query(None, ge=0)]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="Отсутствует токен авторизации")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)
    user_id = data.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="id не найден")
    return user_id


async def get_db():
    async with DBManager(session_factory=async_new_session) as db:
        yield db


PaginationDep = Annotated[PaginationParams, Depends()]
UserIdDep = Annotated[TokenDecodeParams, Depends(get_current_user_id)]
RoomsParamsDep = Annotated[RoomsParams, Depends()]
DBDep = Annotated[DBManager, Depends(get_db)]
