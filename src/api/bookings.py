from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings_schemas import BookingAddRequest
from src.schemas.rooms_schemas import RoomPatchOnly

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все значения таблицы бронирований")
async def get_bookings(db: DBDep):
	return await db.bookings.get_all()


@router.get("/me", summary="Получить бронирования пользователя")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
	return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создать бронирование")
async def make_booking(
	db: DBDep,
	user_id: UserIdDep,
	data: BookingAddRequest = Body(openapi_examples={
		"1": {
			"summary": "Бронирование",
			"value": {
				"room_id": "1",
				"date_from": "01/08/2024",
				"date_to": "10/08/2024",
			}
		},
	})
):
	room_to_booking = await db.rooms.get_one(id=data.room_id)
	booking = await db.bookings.create_booking(user_id=user_id, room=room_to_booking, **data.model_dump())
	await db.commit()
	return {"status": "OK", "data": booking}


@router.delete("/delete/{booking_id}", summary="Удалить бронирование по его id")
async def delete_booking(db: DBDep,	user_id: UserIdDep, booking_id: int):
	await db.bookings.delete(id=booking_id, user_id=user_id)
	await db.commit()
	return {"status": "OK"}
