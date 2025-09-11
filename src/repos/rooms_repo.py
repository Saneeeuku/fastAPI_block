from src.repos.base import BaseRepository
from src.models.rooms_model import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    