from datetime import date

from sqlalchemy import select, delete

from src.models.rooms_model import RoomsOrm
from src.repos.base_repo import BaseRepository
from src.models.hotels_model import HotelsOrm
from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils_repo import get_free_rooms_ids


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_by_time(self, date_from: date, date_to: date, location: str, title: str, limit: int, offset: int):
        free_rooms_ids = get_free_rooms_ids(date_from=date_from, date_to=date_to)
        free_hotels_ids = (
            select(RoomsOrm.hotel_id.label("hotel_id"))
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(free_rooms_ids))
            .group_by(RoomsOrm.hotel_id)
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(free_hotels_ids))
        if location:
            query = query.filter(
                HotelsOrm.location.icontains(location.strip())
            )
        if title:
            query = query.filter(
                HotelsOrm.title.icontains(title.strip())
            )
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        return await self.get_filtered(query)

    async def delete_few(self, location, title):
        del_query = delete(HotelsOrm)
        if location:
            del_query = del_query.filter(
                HotelsOrm.location.icontains(location.strip())
                )
        if title:
            del_query = del_query.filter(
                HotelsOrm.title.icontains(title.strip())
                )
        # print(del_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(del_query)
