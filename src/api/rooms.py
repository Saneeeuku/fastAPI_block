from fastapi import APIRouter, Body

from src.database import async_new_session
from src.repos.rooms_repo import RoomsRepository
from src.schemas.rooms_schemas import RoomPATCH, RoomRequestAdd, RoomAdd, Room
from src.api.dependencies import RoomsParamsDep

router = APIRouter(prefix="/hotels/{hotel_id}", tags=["Номера"])


@router.post("", summary="Добавление номера(ов)", description="Добавление номера (одноместный, двухместный и т.д.), c указанием количества")
async def create_room(hotel_id: int, data: RoomRequestAdd = Body(
	openapi_examples={
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
	async with async_new_session() as session:
		rooms = await RoomsRepository(session).add(new_data)
		await session.commit()
	return {"status": "OK", "data": rooms}


@router.get("/rooms", summary="Найти подходящие номера", description="По параметрам, частичное сравнение")
async def get_rooms(hotel_id: int, data: RoomsParamsDep):
	async with async_new_session() as session:
		rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id, **data.model_dump())
	return rooms


@router.get("/rooms/{room_id}", summary="Получить номер по его id")
async def get_room(hotel_id: int, room_id: int):
	async with async_new_session() as session:
		room = await RoomsRepository(session).get_one(id=room_id, hotel_id=hotel_id)
	return room


@router.put("/rooms/{room_id}", summary="Изменение всех данных номера", description="Все поля обязательны")
async def modify_room(hotel_id: int, room_id: int, data: RoomRequestAdd):
	async with async_new_session() as session:
		await RoomsRepository(session).edit(data, id=room_id, hotel_id=hotel_id)
		await session.commit()
	return {"status": "OK"}


@router.patch("/rooms/{room_id}", summary="Изменение части данных номера")
async def modify_room_partially(hotel_id: int, room_id: int, data: RoomPATCH):
	async with async_new_session() as session:
		await RoomsRepository(session).edit(data, id=room_id, hotel_id=hotel_id, exclude_unset_and_none=True)
		await session.commit()
	return {"status": "OK"}


@router.delete("/rooms/{room_id}", summary="Удаление номера по id")
async def delete_room(hotel_id: int, room_id: int):
	async with async_new_session() as session:
		await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
		await session.commit()
	return {"status": "OK"}
