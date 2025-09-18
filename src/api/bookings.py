from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings_schemas import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создать бронирование")
async def make_booking(
	db: DBDep,
	user_id: UserIdDep,
	data: BookingAddRequest = Body(openapi_examples={
		"1": {
			"summary": "Бронирование",
			"value": {
				"room_id": "7",
				"date_from": "23/04/2025",
				"date_to": "25/04/2025",
			}
		},
	})
):
	room_to_booking = await db.rooms.get_one(id=data.room_id)
	temp_booking = BookingAdd(user_id=user_id, price=room_to_booking.price, **data.model_dump())
	booking = await db.bookings.add(temp_booking)
	await db.commit()
	return {"status": "OK", "data": booking}


@router.get("", summary="Получить все значения таблицы бронирований")
async def get_bookings(db: DBDep):
	return await db.bookings.get_all()


@router.get("/me", summary="Получить бронирования пользователя")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
	return await db.bookings.get_all_by_id(user_id)
