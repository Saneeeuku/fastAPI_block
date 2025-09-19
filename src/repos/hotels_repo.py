from datetime import date
from typing import cast

from sqlalchemy import select, delete

from src.models.rooms_model import RoomsOrm
from src.repos.base_repo import BaseRepository
from src.models.hotels_model import HotelsOrm
from src.repos.utils_repo import get_free_rooms_ids
from src.schemas.hotels_schemas import Hotel


def _get_by_params(location, title):
    query = select(HotelsOrm.id.label("hotel_id"))
    if location:
        query = query.filter(
            HotelsOrm.location.icontains(location.strip())
            )
    if title:
        query = query.filter(
            HotelsOrm.title.icontains(title.strip())
            )
    return query.cte(name="hotels_by_params")


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_by_time(self, date_from: date, date_to: date, location: str, title: str, limit: int, offset: int):
        free_rooms_ids = get_free_rooms_ids(date_from=date_from, date_to=date_to)
        free_hotels_ids = (
            select(RoomsOrm.hotel_id.label("hotel_id"))
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(free_rooms_ids))
            .group_by(RoomsOrm.hotel_id)
            .cte(name="free_hotels_ids")
        )
        hotels_by_params = _get_by_params(location, title)
        combined = (
            select(free_hotels_ids.c.hotel_id)
            .select_from(hotels_by_params)
            .outerjoin(free_hotels_ids,
                       cast("ColumnElement[bool]", free_hotels_ids.c.hotel_id == hotels_by_params.c.hotel_id))
            .limit(limit)
            .offset(offset)
        )
        # print(free_hotels_ids.compile(compile_kwargs={"literal_binds": True}))
        # print(hotels_by_params.compile(compile_kwargs={"literal_binds": True}))
        # print(combined.compile(compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(HotelsOrm.id.in_(combined))

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
