from datetime import datetime

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsORM
from src.schemas.bookings_schemas import Booking, BookingAdd, BookingWDate


class BookingsRepository(BaseRepository):
	model = BookingsORM
	schema = Booking

	async def add(self, data: BookingAdd):
		try:
			temp_booking = BookingWDate(
				user_id=data.user_id, room_id=data.room_id,
				date_from=datetime.strptime(data.date_from, "%d/%m/%Y"),
				date_to=datetime.strptime(data.date_to, "%d/%m/%Y"),
				price=data.price)
			temp_booking.price = temp_booking.total_cost
		except ValidationError:
			raise HTTPException(status_code=401)
		add_stmt = (
			insert(self.model)
			.values(**temp_booking.model_dump())
			.returning(self.model)
		)
		try:
			result = await self.session.execute(add_stmt)
		except IntegrityError as e:
			raise HTTPException(status_code=422,
								detail=f"{e.__class__.__name__}: {e.orig.args[0].split('DETAIL:  ')[1]}")
		result = result.scalars().one()
		return self.schema.model_validate(result, from_attributes=True)
