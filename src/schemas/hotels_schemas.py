from pydantic import BaseModel, Field, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int

    # model_config = ConfigDict(from_attributes=True) как вариант, вместо прописывания в repos/base.py


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)
