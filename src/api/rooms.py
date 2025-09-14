from fastapi import APIRouter, Body, Query

from src.database import async_new_session
from src.repos.rooms_repo import RoomsRepository
from src.schemas.rooms_schemas import RoomRequestAdd, RoomAdd, Room
from src.api.dependencies import RoomsParamsDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("{hotel_id}/rooms", summary="Найти подходящие номера", description="Найти номера по параметрам")
async def get_all_rooms(hotel_id: int, data: RoomsParamsDep):
	async with async_new_session() as session:
		rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id, **data.model_dump())
	return rooms


@router.post("/{hotel_id}", summary="Добавление номера(ов)",
			 description="Добавление номера (одноместный, двухместный и т.д.), или нескольких (указанного количества)")
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
		"summary": "Одноместный",
		"value": {
			"title": "Двухместный, 1 кровать",
			"description": "Номер с одной кроватью для двух человек",
			"price": 7000,
			"quantity": 2,
		}
	},
	"3": {
		"summary": "Одноместный",
		"value": {
			"title": "Двухместный, 2 кровать",
			"description": "Номер с двумя кроватями для двух человек",
			"price": 10000,
			"quantity": 10,
		}
	},
	"4": {
		"summary": "Одноместный",
		"value": {
			"title": "Президентский",
			"description": "Элита элитная с видном на космос",
			"price": 9999999999,
			"quantity": 1,
		}
	},
	})):
	new_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
	async with async_new_session() as session:
		rooms = await RoomsRepository(session).add(new_data)
		await session.commit()
	return {"status": "OK", "data": rooms}



#
#
# @router.get("/{hotel_id}")
# async def get_rooms(hotel_id: int):
# 	...
#
#
# @router.put("/{hotel_id}/rooms/{room_id}")
# async def modify_room(hotel_id: int, room_id: int):
# 	...
#
#
# @router.patch("/{hotel_id}/rooms/{room_id}")
# async def modify_room_partially(hotel_id: int, room_id: int):
# 	...
#
#
# @router.delete("/{hotel_id}/rooms")
# async def delete_rooms(hotel_id: int, room_id: int):
# 	...
