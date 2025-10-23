from datetime import date

from sqlalchemy import func, select

from src.models.bookings_model import BookingsOrm
from src.models.rooms_model import RoomsOrm


def get_free_rooms_ids(date_from: date, date_to: date, hotel_id: int | None = None):
    booked_rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("booked_rooms"))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
        .group_by(BookingsOrm.room_id)
        .cte(name="booked_rooms_count")
    )
    # print(booked_rooms_count.compile(compile_kwargs={"literal_binds": True}))
    rooms_left_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(booked_rooms_count.c.booked_rooms, 0)).label(
                "rooms_left"
            ),
        )
        .select_from(RoomsOrm)
        .outerjoin(booked_rooms_count, RoomsOrm.id == booked_rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )
    rooms_ids = select(RoomsOrm.id).select_from(RoomsOrm)
    if hotel_id is not None:
        rooms_ids = rooms_ids.filter_by(hotel_id=hotel_id)

    rooms_ids = rooms_ids.subquery(name="rooms_ids")
    free_rooms_ids = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0, rooms_left_table.c.room_id.in_(select(rooms_ids))
        )
    )
    return free_rooms_ids
