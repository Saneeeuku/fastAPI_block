from pydantic import EmailStr
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.users_model import UsersOrm
from src.schemas.users_schemas import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        result = result.scalars().one()
        return UserWithHashedPassword.model_validate(result, from_attributes=True)
