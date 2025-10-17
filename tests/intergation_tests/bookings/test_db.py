import datetime

from src.schemas.bookings_schemas import BookingAdd, Booking


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    print(user_id, room_id)
    data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.date(2025, 10, 18),
        date_to=datetime.date(2025, 10, 25),
        price=5000)
    res = await db.bookings.add(data)
    await db.commit()
    assert res and Booking.model_validate(res)
