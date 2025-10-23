from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities_schemas import FacilityRequestAdd
# from src.utils.self_cache_deco import my_cache

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить всю таблицу удобств")
@cache(expire=10)
# @my_cache(expire=5)
async def get_all(db: DBDep):
    return await db.facilities.get_all()


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
    fac = await db.facilities.add(data=data)
    await db.commit()
    return {"status": "OK", "data": fac}
