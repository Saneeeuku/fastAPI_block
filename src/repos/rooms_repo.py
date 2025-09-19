from datetime import date

from sqlalchemy import func, select

from src.repos.base_repo import BaseRepository
from src.models.rooms_model import RoomsOrm
from src.schemas.rooms_schemas import Room
from src.repos.utils_repo import get_free_rooms_ids


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

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
        return [self.schema.model_validate(model, from_attributes=True) for
                model in result.scalars().all()]

    async def get_by_time(self, hotel_id: int, date_from: date, date_to: date):
        free_rooms = get_free_rooms_ids(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(free_rooms))
