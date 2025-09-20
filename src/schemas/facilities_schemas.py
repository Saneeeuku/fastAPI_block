from pydantic import BaseModel


class FacilityRequestAdd(BaseModel):
    title: str


class Facility(FacilityRequestAdd):
    id: int


class RoomFacilityRequestAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityRequestAdd):
    id: int
