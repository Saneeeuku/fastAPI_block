from pydantic import BaseModel


class RoomRequestAdd(BaseModel):
	title: str
	description: str | None = None
	price: int
	quantity: int


class RoomAdd(RoomRequestAdd):
	hotel_id: int


class Room(RoomRequestAdd):
	id: int


class RoomPATCH(BaseModel):
	title: str | None = None
	description: str | None = None
	price: int | None = None
	quantity: int | None = None
