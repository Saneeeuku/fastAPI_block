from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import NoFreeRoomsException, ObjectNotFoundException
from src.schemas.bookings_schemas import BookingAddRequest
from src.services.bookings_service import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все значения таблицы бронирований")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get("/me", summary="Получить бронирования пользователя")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingsService(db).get_user_bookings(user_id)


@router.post("", summary="Создать бронирование")
async def make_booking(
    db: DBDep,
    user_id: UserIdDep,
    data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Бронирование",
                "value": {
                    "room_id": "1",
                    "date_from": "01/08/2024",
                    "date_to": "10/08/2024",
                },
            },
        }
    ),
):
    try:
        booking = await BookingsService(db).make_booking(user_id, data)
    except (ObjectNotFoundException, NoFreeRoomsException) as e:
        if isinstance(e, ObjectNotFoundException):
            raise HTTPException(status_code=404, detail="Номер не найден")
        elif isinstance(e, NoFreeRoomsException):
            raise HTTPException(status_code=404, detail=e.detail)
        else:
            raise e
    return {"status": "OK", "data": booking}


@router.delete("/delete/{booking_id}", summary="Удалить бронирование по его id")
async def delete_booking(db: DBDep, user_id: UserIdDep, booking_id: int):
    await BookingsService(db).delete_booking(user_id, booking_id)
    return {"status": "OK"}
