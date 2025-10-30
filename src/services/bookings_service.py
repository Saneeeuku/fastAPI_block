from src.api.dependencies import UserIdDep
from src.schemas.bookings_schemas import BookingAddRequest
from src.services.base_service import BaseService


class BookingsService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def make_booking(self, user_id: UserIdDep, data: BookingAddRequest):
        room_to_booking = await self.db.rooms.get_one(id=data.room_id)
        booking = await self.db.bookings.create_booking(
            user_id=user_id, room=room_to_booking, **data.model_dump()
        )
        await self.db.commit()
        return booking

    async def delete_booking(self, user_id: UserIdDep, booking_id: int):
        await self.db.bookings.delete(id=booking_id, user_id=user_id)
        await self.db.commit()
