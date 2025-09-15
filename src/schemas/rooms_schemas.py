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


class RoomPATCH(BaseModel):
	title: str | None = Field(default=None)
	description: str | None = Field(default=None)
	price: int | None = Field(default=None)
	quantity: int | None = Field(default=None)
