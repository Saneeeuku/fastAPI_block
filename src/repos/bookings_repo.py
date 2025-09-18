from sqlalchemy import select

from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsORM
from src.schemas.bookings_schemas import Booking


class BookingsRepository(BaseRepository):
	model = BookingsORM
	schema = Booking


	async def get_all_by_id(self, user_id: int):
		query = select(self.model).filter_by(user_id=user_id)
		result = await self.session.execute(query)
		return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
