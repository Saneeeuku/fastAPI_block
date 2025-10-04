from datetime import date

from sqlalchemy import select

from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsOrm
from src.repos.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
	model = BookingsOrm
	mapper = BookingDataMapper
	
	async def get_today_checkins(self):
		query = (
			select(self.model)
			.filter(self.model.date_from == date.today())
		)
		res = await self.session.execute(query)
		return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]
