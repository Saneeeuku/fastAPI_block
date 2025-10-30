from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.exceptions import DateViolationException, RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms_schemas import RoomPatchWithFacilities, RoomRequestAdd
from src.api.dependencies import RoomsParamsDep, DBDep
from src.services.rooms_service import RoomsService

router = APIRouter(prefix="/hotels/{hotel_id}", tags=["Номера"])


@router.post(
    "",
    summary="Добавление номера(ов)",
    description="Добавление номера (одноместный, двухместный и т.д.), c указанием количества",
)
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Одноместный",
                "value": {
                    "title": "Одноместный",
                    "description": "Номер с одной кроватью для одного человека",
                    "price": 5000,
                    "quantity": 1,
                    "facilities_ids": [1, 2, 3],
                },
            },
            "2": {
                "summary": "Двухместный",
                "value": {
                    "title": "Двухместный, 1 кровать",
                    "description": "Номер с одной кроватью для двух человек",
                    "price": 7000,
                    "quantity": 2,
                    "facilities_ids": [1, 2, 3],
                },
            },
            "3": {
                "summary": "Двухместный",
                "value": {
                    "title": "Двухместный, 2 кровати",
                    "description": "Номер с двумя кроватями для двух человек",
                    "price": 10000,
                    "quantity": 10,
                    "facilities_ids": [1, 2, 3],
                },
            },
            "4": {
                "summary": "Элитный",
                "value": {
                    "title": "Президентский",
                    "description": "Элита элитная с видном на космос",
                    "price": 9_999_999,
                    "quantity": 1,
                    "facilities_ids": [1, 2, 3],
                },
            },
        }
    ),
):
    try:
        room = await RoomsService(db).create_room(hotel_id, data)
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK", "data": room}


@router.get(
    "/rooms",
    summary="Найти подходящие номера",
    description="По названию, описанию (частичное сравнение) и (или) цене",
)
async def get_rooms(db: DBDep, hotel_id: int, data: RoomsParamsDep):
    try:
        rooms = await RoomsService(db).get_rooms(hotel_id, data)
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK", "data": rooms}


@router.get("/rooms/free", summary="Найти подходящие по времени свободные номера")
async def get_free_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(
        openapi_examples={"1": {"value": "2024-08-01"}},
        description="Формат даты (год-месяц-число) и разделитель менять нельзя",
    ),
    date_to: date = Query(
        openapi_examples={"1": {"value": "2024-08-10"}},
        description="Формат даты (год-месяц-число) и разделитель менять нельзя",
    ),
):
    try:
        rooms = await RoomsService(db).get_free_rooms(hotel_id, date_from, date_to)
    except (DateViolationException, HotelNotFoundException) as e:
        if isinstance(e, DateViolationException):
            raise HTTPException(status_code=412, detail=e.detail)
        elif isinstance(e, HotelNotFoundException):
            raise HTTPException(status_code=404, detail=e.detail)
        else:
            raise e
    return {"status": "OK", "data": rooms}


@router.get("/rooms/{room_id}", summary="Получить номер по его id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        room = await RoomsService(db).get_room(hotel_id, room_id)
    except (HotelNotFoundException, RoomNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK", "data": room}


@router.put(
    "/rooms/{room_id}", summary="Изменение всех данных номера", description="Все поля обязательны"
)
async def modify_room(db: DBDep, hotel_id: int, room_id: int, data: RoomRequestAdd):
    try:
        await RoomsService(db).modify_room(hotel_id, room_id, data)
    except (HotelNotFoundException, RoomNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}


@router.patch("/rooms/{room_id}", summary="Изменение части данных номера")
async def modify_room_partially(
    db: DBDep, hotel_id: int, room_id: int, data: RoomPatchWithFacilities
):
    try:
        await RoomsService(db).modify_room_partially(hotel_id, room_id, data)
    except (HotelNotFoundException, RoomNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}


@router.delete("/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomsService(db).delete_room(hotel_id, room_id)
    except (HotelNotFoundException, RoomNotFoundException) as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}
