from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic_core import ValidationError


class BookingAddRequest(BaseModel):
	room_id: int
	date_from: str
	date_to: str


class BookingAdd(BaseModel):
	user_id: int
	room_id: int
	date_from: datetime
	date_to: datetime
	price: int

	def __init__(self, **data):
		try:
			data["date_from"] = datetime.strptime(data.get("date_from"), "%d/%m/%Y")
			data["date_to"] = datetime.strptime(data.get("date_to"), "%d/%m/%Y")
		except ValidationError:
			raise HTTPException(status_code=401)
		super().__init__(**data)
		self.price = self.total_cost

	@property
	def total_cost(self):
		return self.price * (self.date_to - self.date_from).days


class Booking(BookingAdd):
	id: int
