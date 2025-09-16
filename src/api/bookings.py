from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings_schemas import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def make_booking(db: DBDep, user_id: UserIdDep, data: BookingAddRequest):
	room_to_booking = db.rooms.get_one(data.room_id)
	temp_booking = BookingAdd(user_id=user_id, **room_to_booking)  # db.bookings.model.total_cost
	print(temp_booking)
