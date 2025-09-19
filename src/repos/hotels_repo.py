from datetime import date

from sqlalchemy import select, delete

from src.models.rooms_model import RoomsOrm
from src.repos.base_repo import BaseRepository
from src.models.hotels_model import HotelsOrm
from src.repos.utils_repo import get_free_rooms_ids
from src.schemas.hotels_schemas import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
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
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_by_time(self, date_from: date, date_to: date):
        free_rooms_ids = get_free_rooms_ids(date_from=date_from, date_to=date_to)
        free_hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(free_rooms_ids))
            .group_by(RoomsOrm.hotel_id)
        )
        # print(free_hotels_ids.compile(compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(HotelsOrm.id.in_(free_hotels_ids))

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
