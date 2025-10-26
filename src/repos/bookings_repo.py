from datetime import date

from sqlalchemy import select

from src.exceptions import NoFreeRoomsException, DateViolationException
from src.repos.base_repo import BaseRepository
from src.models.bookings_model import BookingsOrm
from src.repos.mappers.mappers import BookingDataMapper
from src.repos.utils_repo import get_free_rooms_ids
from src.schemas.bookings_schemas import BookingAdd
from src.schemas.rooms_schemas import RoomWithRels


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_today_checkins(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def create_booking(
        self, user_id, room: RoomWithRels, date_from: str, date_to: str, **kwargs
    ):
        temp_booking = BookingAdd(
            user_id=user_id, room_id=room.id, date_from=date_from, date_to=date_to, price=room.price
        )
        try:
            free_rooms_ids = await self.session.execute(
                get_free_rooms_ids(temp_booking.date_from, temp_booking.date_to)
            )
        except DateViolationException as e:
            raise e
        if room.id not in free_rooms_ids.scalars().all():
            raise NoFreeRoomsException
        else:
            return await self.add(temp_booking)
