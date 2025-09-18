from datetime import date

from fastapi import APIRouter, Body, Query

from src.schemas.rooms_schemas import RoomPATCH, RoomRequestAdd, RoomAdd
from src.api.dependencies import RoomsParamsDep, DBDep

router = APIRouter(prefix="/hotels/{hotel_id}", tags=["Номера"])


@router.post("", summary="Добавление номера(ов)",
             description="Добавление номера (одноместный, двухместный и т.д.),"
                         " c указанием количества")
async def create_room(db: DBDep, hotel_id: int,
                      data: RoomRequestAdd = Body(openapi_examples={
                          "1": {
                              "summary": "Одноместный",
                              "value": {
                                  "title": "Одноместный",
                                  "description": "Номер с одной кроватью для одного человека",
                                  "price": 5000,
                                  "quantity": 1,
                              }
                          },
                          "2": {
                              "summary": "Двухместный",
                              "value": {
                                  "title": "Двухместный, 1 кровать",
                                  "description": "Номер с одной кроватью для двух человек",
                                  "price": 7000,
                                  "quantity": 2,
                              }
                          },
                          "3": {
                              "summary": "Двухместный",
                              "value": {
                                  "title": "Двухместный, 2 кровати",
                                  "description": "Номер с двумя кроватями для двух человек",
                                  "price": 10000,
                                  "quantity": 10,
                              }
                          },
                          "4": {
                              "summary": "Элитный",
                              "value": {
                                  "title": "Президентский",
                                  "description": "Элита элитная с видном на космос",
                                  "price": 9_999_999,
                                  "quantity": 1,
                              }
                          },
                      })):
    new_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    rooms = await db.rooms.add(new_data)
    await db.commit()
    return {"status": "OK", "data": rooms}


@router.get("/rooms", summary="Найти подходящие номера",
            description="По названию, описанию (частичное сравнение), и (или) цене")
async def get_rooms(db: DBDep, hotel_id: int, data: RoomsParamsDep):
    rooms = await db.rooms.get_all(hotel_id=hotel_id, **data.model_dump())
    return rooms


@router.get("/rooms/free",
            summary="Найти подходящие по времени свободные номера")
async def get_free_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10")
):
    rooms = await db.rooms.get_by_time(hotel_id=hotel_id, date_from=date_from,
                                       date_to=date_to)
    return rooms


@router.get("/rooms/{room_id}", summary="Получить номер по его id")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    return room


@router.put("/rooms/{room_id}", summary="Изменение всех данных номера",
            description="Все поля обязательны")
async def modify_room(db: DBDep, hotel_id: int, room_id: int,
                      data: RoomRequestAdd):
    await db.rooms.edit(data, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/rooms/{room_id}", summary="Изменение части данных номера")
async def modify_room_partially(db: DBDep, hotel_id: int, room_id: int,
                                data: RoomPATCH):
    await db.rooms.edit(data, id=room_id, hotel_id=hotel_id,
                        exclude_unset_and_none=True)
    await db.commit()
    return {"status": "OK"}


@router.delete("/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
