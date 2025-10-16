from src.database import async_new_session
from src.schemas.hotels_schemas import HotelAdd
from src.utils.db_manager import DBManager


async def test_hotel_add():
    data = HotelAdd(title="title1", location="location1")
    async with DBManager(session_factory=async_new_session) as db:
        await db.hotels.add(data)
        await db.commit()
