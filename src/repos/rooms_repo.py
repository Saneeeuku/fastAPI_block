from datetime import date

from sqlalchemy import func, select

from src.database import engine
from src.models.bookings_model import BookingsOrm
from src.repos.base_repo import BaseRepository
from src.models.rooms_model import RoomsOrm
from src.schemas.rooms_schemas import Room, RoomRequestAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id: int, title: str, description: str,
                      price: int):
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
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_count = (
            select(BookingsOrm.room_id,
                   func.count("*").label("booked_rooms"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )
        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.booked_rooms, 0)).label("rooms_left"),
                )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        rooms_ids = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids")
        )
        query = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0,
                    rooms_left_table.c.room_id.in_(rooms_ids)
            )
        )
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsOrm.id.in_(query))
