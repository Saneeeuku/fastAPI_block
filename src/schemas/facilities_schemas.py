from pydantic import BaseModel


class FacilityRequestAdd(BaseModel):
    title: str


class Facility(FacilityRequestAdd):
    id: int
