import datetime

from src.schemas.bookings_schemas import BookingAdd, Booking


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.date(2025, 10, 18),
        date_to=datetime.date(2025, 10, 25),
        price=5000)
    booking = await db.bookings.add(data)
    assert booking and isinstance(booking, Booking)

    res = await db.bookings.get_one(id=booking.id)
    assert res and isinstance(res, Booking)

    data.date_to = datetime.date(2025, 10, 26)
    await db.bookings.edit(data, id=res.id)
    booking = await db.bookings.get_one(id=res.id)
    assert (booking and
            isinstance(booking, Booking) and
            booking.date_to == data.date_to
            )

    await db.bookings.delete(id=res.id)
    deleted = await db.bookings.get_one_or_none(id=booking.id)
    assert deleted is None

    await db.commit()
