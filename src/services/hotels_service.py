from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels_schemas import HotelAdd, HotelPatch
from src.services.base_service import BaseService


class HotelsService(BaseService):

    async def get_hotels(self):
        return await self.db.hotels.get_all()

    async def get_hotel(self, _id: int):
        try:
            return await self.db.hotels.get_one(id=_id)
        except ObjectNotFoundException as e:
            raise HotelNotFoundException from e

    async def get_free_hotels(
        self,
        date_from: date,
        date_to: date,
        title: str | None,
        location: str | None,
        pagination: PaginationDep,
    ):
        return await self.db.hotels.get_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
        )

    async def create_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def change_hotel(self, _id: int, data: HotelAdd):
        await self.db.hotels.edit(data, id=_id)
        await self.db.commit()

    async def change_hotel_partially(self, _id: int, data: HotelPatch):
        await self.db.hotels.edit(data, id=_id, exclude_unset_and_none=True)
        await self.db.commit()

    async def delete_hotel(self, _id: int):
        await self.db.hotels.delete(id=_id)
        await self.db.commit()

    async def delete_few_hotels(self, title: str | None, location: str | None):
        await self.db.hotels.delete_few(title=title, location=location)
        await self.db.commit()
