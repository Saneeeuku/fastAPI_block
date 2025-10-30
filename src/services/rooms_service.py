from datetime import date

from src.api.dependencies import RoomsParamsDep
from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.facilities_schemas import RoomFacilityRequestAdd
from src.schemas.rooms_schemas import RoomRequestAdd, RoomAdd, RoomPatchWithFacilities, RoomPatchOnly
from src.services.base_service import BaseService
from src.services.hotels_service import HotelsService


class RoomsService(BaseService):
    async def create_room(self, hotel_id: int, data: RoomRequestAdd):
        await HotelsService(self.db).get_hotel(hotel_id)

        new_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        rooms = await self.db.rooms.add(new_data)
        room_facilities = [
            RoomFacilityRequestAdd(room_id=rooms.id, facility_id=el) for el in data.facilities_ids
        ]
        if room_facilities:
            await self.db.room_facilities.add_bulk(room_facilities)
        await self.db.commit()
        return rooms

    async def get_rooms(self, hotel_id: int, data: RoomsParamsDep):
        await HotelsService(self.db).get_hotel(hotel_id)

        rooms = await self.db.rooms.get_all_with_filters(hotel_id=hotel_id, **data.model_dump())
        return rooms

    async def get_free_rooms( self, hotel_id: int, date_from: date, date_to: date):
        await HotelsService(self.db).get_hotel(hotel_id)

        rooms = await self.db.rooms.get_by_time(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
        return rooms

    async def get_room(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).get_hotel(hotel_id)

        room = await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        return room

    async def modify_room(self, hotel_id: int, room_id: int, data: RoomRequestAdd):
        await HotelsService(self.db).get_hotel(hotel_id)

        room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        try:
            await self.db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e
        await self.db.room_facilities.change_facilities(room_id=room_id, facilities_ids=data.facilities_ids)
        await self.db.commit()

    async def modify_room_partially(
        self, hotel_id: int, room_id: int, data: RoomPatchWithFacilities
    ):
        await HotelsService(self.db).get_hotel(hotel_id)

        room_only_data = RoomPatchOnly(**data.model_dump())
        try:
            if any(v is not None for _, v in room_only_data):
                await self.db.rooms.edit(
                    room_only_data, id=room_id, hotel_id=hotel_id, exclude_unset_and_none=True
                )
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e
        if data.facilities_ids:
            await self.db.room_facilities.change_facilities(room_id=room_id, facilities_ids=data.facilities_ids)
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).get_hotel(hotel_id)

        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e
        await self.db.commit()
