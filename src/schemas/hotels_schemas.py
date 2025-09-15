from pydantic import BaseModel, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int

    # model_config = ConfigDict(from_attributes=True) как вариант, вместо прописывания в repos/base_repo.py


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
