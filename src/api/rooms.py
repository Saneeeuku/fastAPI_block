from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.exceptions import DateViolationException, DataConflictException, ObjectNotFoundException
from src.schemas.facilities_schemas import RoomFacilityRequestAdd
from src.schemas.rooms_schemas import (
    RoomPatchWithFacilities,
    RoomRequestAdd,
    RoomAdd,
    RoomPatchOnly,
)
from src.api.dependencies import RoomsParamsDep, DBDep

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
    new_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    try:
        rooms = await db.rooms.add(new_data)
    except DataConflictException:
        raise HTTPException(status_code=404, detail="Отель не найден")
    room_facilities = [
        RoomFacilityRequestAdd(room_id=rooms.id, facility_id=el) for el in data.facilities_ids
    ]
    if room_facilities:
        await db.room_facilities.add_bulk(room_facilities)
    await db.commit()
    return {"status": "OK", "data": rooms}


@router.get(
    "/rooms",
    summary="Найти подходящие номера",
    description="По названию, описанию (частичное сравнение), и (или) цене",
)
async def get_rooms(db: DBDep, hotel_id: int, data: RoomsParamsDep):
    rooms = await db.rooms.get_all_with_filters(hotel_id=hotel_id, **data.model_dump())
    return rooms


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
        rooms = await db.rooms.get_by_time(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
    except DateViolationException as e:
        raise HTTPException(status_code=412, detail=e.detail)
    return rooms


@router.get("/rooms/{room_id}", summary="Получить номер по его id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        room = await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return room


@router.put(
    "/rooms/{room_id}", summary="Изменение всех данных номера", description="Все поля обязательны"
)
async def modify_room(db: DBDep, hotel_id: int, room_id: int, data: RoomRequestAdd):
    room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    try:
        await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.room_facilities.change_facilities(room_id=room_id, facilities_ids=data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/rooms/{room_id}", summary="Изменение части данных номера")
async def modify_room_partially(
    db: DBDep, hotel_id: int, room_id: int, data: RoomPatchWithFacilities
):
    room_only_data = RoomPatchOnly(**data.model_dump())
    if any(v is not None for _, v in room_only_data):
        try:
            await db.rooms.edit(
                room_only_data, id=room_id, hotel_id=hotel_id, exclude_unset_and_none=True
            )
        except ObjectNotFoundException:
            raise HTTPException(status_code=404, detail="Номер не найден")
    if data.facilities_ids:
        await db.room_facilities.change_facilities(
            room_id=room_id, facilities_ids=data.facilities_ids
        )
    await db.commit()
    return {"status": "OK"}


@router.delete("/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.commit()
    return {"status": "OK"}
