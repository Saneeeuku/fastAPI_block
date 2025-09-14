from sqlalchemy import select

from src.repos.base_repo import BaseRepository
from src.models.rooms_model import RoomsOrm
from src.schemas.rooms_schemas import Room, RoomRequestAdd


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
        return [RoomRequestAdd.model_validate(model, from_attributes=True) for model in result.scalars().all()]