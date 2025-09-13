from typing import Annotated

from pydantic import BaseModel
from fastapi import Query, Depends, Request, HTTPException

from src.services.auth_service import AuthService


class PaginationParams(BaseModel):
	page: Annotated[int | None, Query(1, gt=0)]
	per_page: Annotated[int | None, Query(5, gt=0, le=30)]


class TokenDecodeParams(BaseModel):
	id: int
	nickname: str


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


PaginationDep = Annotated[PaginationParams, Depends()]
UserIdDep = Annotated[TokenDecodeParams, Depends(get_current_user_id)]
