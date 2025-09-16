from datetime import datetime

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
	room_id: int
	date_from: datetime
	date_to: datetime


class BookingAdd(BookingAddRequest):
	user_id: int
	price: int


class Booking(BookingAddRequest):
	id: int
