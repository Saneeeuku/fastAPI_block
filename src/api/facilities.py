from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities_schemas import FacilityRequestAdd
from src.services.facilities_service import FacilitiesService

# from src.utils.self_cache_deco import my_cache

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить всю таблицу удобств")
@cache(expire=10)
# @my_cache(expire=5)
async def get_facilities(db: DBDep):
    return await FacilitiesService(db).get_facilities()


@router.post("", summary="Добавить одно из удобств")
@cache(expire=10)
# @my_cache(expire=10)
async def create_facility(
    db: DBDep,
    data: FacilityRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Удобство",
                "value": {
                    "title": "Удобство",
                },
            }
        }
    ),
):
    facility = await FacilitiesService(db).create_facility(data)
    return {"status": "OK", "data": facility}
