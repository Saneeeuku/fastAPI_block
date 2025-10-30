from src.schemas.facilities_schemas import FacilityRequestAdd
from src.services.base_service import BaseService


class FacilitiesService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityRequestAdd):
        fac = await self.db.facilities.add(data=data)
        await self.db.commit()
        return fac
