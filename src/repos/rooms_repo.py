from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repos.base_repo import BaseRepository
from src.models.rooms_model import RoomsOrm
from src.repos.mappers.mappers import RoomDataMapper
from src.schemas.rooms_schemas import Room, RoomWithRels
from src.repos.utils_repo import get_free_rooms_ids


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_all(self, hotel_id: int, title: str, description: str, price: int):
        query = select(self.model).filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(
                self.model.title.icontains(title.strip())
            )
        if description:
            query = query.filter(
                self.model.description.icontains(description.strip())
            )
        if price:
            query = query.where(self.model.price <= price)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one(self, **filters):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filters)
        )
        result = await self.session.execute(query)
        result = await self.get_one_query_result(result)
        return RoomWithRels.model_validate(result, from_attributes=True)

    async def get_by_time(self, hotel_id: int, date_from: date, date_to: date):
        free_rooms = get_free_rooms_ids(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(free_rooms))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]