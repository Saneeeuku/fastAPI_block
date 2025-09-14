from pydantic import BaseModel, Field


class RoomRequestAdd(BaseModel):
	title: str
	description: str | None
	price: int
	quantity: int


class RoomAdd(RoomRequestAdd):
	hotel_id: int


class Room(RoomRequestAdd):
	id: int
