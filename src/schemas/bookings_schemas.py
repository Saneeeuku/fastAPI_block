from datetime import date, datetime

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
    date_from: date
    date_to: date
    price: int

    def __init__(self, **data):
        if not all([isinstance(el, date) for el in (data["date_from"], data["date_to"])]):
            try:
                data["date_from"] = _convert_str_to_date(data.get("date_from"))
                data["date_to"] = _convert_str_to_date(data.get("date_to"))
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=e.args)
        super().__init__(**data)
        self.price = self.total_cost

    @property
    def total_cost(self):
        return self.price * (self.date_to - self.date_from).days


class Booking(BookingAdd):
    id: int
    created_at: datetime


def _convert_str_to_date(str_date: str):
    if not str_date:
        raise ValidationError("Неверный формат даты")
    sep = "-"
    for el in str_date:
        if el in ".,/":
            sep = el
            break
    formats = [f"%Y{sep}%m{sep}%d", f"%d{sep}%m{sep}%Y"]
    formatted_date = None
    for f in formats:
        try:
            formatted_date = datetime.strptime(str_date, f).date()
        except ValueError:
            continue
    if formatted_date is None:
        raise ValidationError("Неверный формат даты")
    else:
        return formatted_date
