from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.repos.base_repo import BaseRepository
from src.models.users_model import UsersOrm
from src.repos.mappers.mappers import UsersDataMapper
from src.schemas.users_schemas import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            result = result.scalars().one()
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=f"Пользователь не найден. {e.args}")
        return UserWithHashedPassword.model_validate(result, from_attributes=True)
