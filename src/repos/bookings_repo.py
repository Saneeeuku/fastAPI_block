from sqlalchemy import select

from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsOrm
from src.schemas.bookings_schemas import Booking


class BookingsRepository(BaseRepository):
	model = BookingsOrm
	schema = Booking
