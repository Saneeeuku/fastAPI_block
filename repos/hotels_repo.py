from sqlalchemy import select

from repos.base import BaseRepository
from src.models.hotels_model import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        if location:
            query = query.filter(
                HotelsOrm.location.icontains(location.strip())
                )
        if title:
            query = query.filter(
                HotelsOrm.title.icontains(title.strip())
                )
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
