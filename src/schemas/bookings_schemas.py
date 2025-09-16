from datetime import datetime

from pydantic import BaseModel


class BookingAddRequest(BaseModel):
	room_id: int
	date_from: str
	date_to: str


class BookingAdd(BookingAddRequest):
	user_id: int
	price: int


class BookingWDate(BaseModel):
	user_id: int
	room_id: int
	date_from: datetime
	date_to: datetime
	price: int

	@property
	def total_cost(self):
		return self.price * (self.date_to - self.date_from).days


class Booking(BookingWDate):
	id: int
