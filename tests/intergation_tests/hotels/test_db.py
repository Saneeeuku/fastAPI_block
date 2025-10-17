from src.schemas.hotels_schemas import HotelAdd


async def test_hotel_add(db):
    data = HotelAdd(title="title1", location="location1")
    await db.hotels.add(data)
    await db.commit()
