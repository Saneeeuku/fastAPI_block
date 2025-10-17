from pydantic import BaseModel

from src.schemas.facilities_schemas import Facility


class RoomRequestAdd(BaseModel):
	title: str
	description: str | None = None
	price: int
	quantity: int
	facilities_ids: list[int] = []


class RoomAdd(BaseModel):
	hotel_id: int
	title: str
	description: str | None = None
	price: int
	quantity: int


class Room(RoomAdd):
	id: int


class RoomWithRels(RoomAdd):
	id: int
	facilities: list[Facility]


class RoomPatchOnly(BaseModel):
	title: str | None = None
	description: str | None = None
	price: int | None = None
	quantity: int | None = None


class RoomPatchWithFacilities(RoomPatchOnly):
	facilities_ids: list[int] = []
