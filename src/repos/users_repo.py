from src.repos.base import BaseRepository
from src.models.users_model import UsersOrm
from src.schemas.users_schemas import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
