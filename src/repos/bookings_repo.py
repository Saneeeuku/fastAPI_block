from sqlalchemy import select

from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsORM
from src.schemas.bookings_schemas import Booking


class BookingsRepository(BaseRepository):
	model = BookingsORM
	schema = Booking
