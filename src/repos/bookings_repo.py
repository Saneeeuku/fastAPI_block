from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsOrm
from src.repos.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
	model = BookingsOrm
	mapper = BookingDataMapper
