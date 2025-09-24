from pydantic import BaseModel


class RoomRequestAdd(BaseModel):
	title: str
	description: str | None = None
	price: int
	quantity: int
	facilities_ids: list[int] | None = None


class RoomAdd(BaseModel):
	hotel_id: int
	title: str
	description: str | None = None
	price: int
	quantity: int


class Room(RoomAdd):
	id: int


class RoomPatchOnly(BaseModel):
	title: str | None = None
	description: str | None = None
	price: int | None = None
	quantity: int | None = None


class RoomPatchWithFacilities(RoomPatchOnly):
	facilities_ids: list[int] | None = None
