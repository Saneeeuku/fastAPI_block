from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities_schemas import FacilityRequestAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получить всю таблицу удобств")
async def get_all(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавить одно из удобств")
async def create_facility(db: DBDep, data: FacilityRequestAdd = Body(openapi_examples={
                          "1": {
                              "summary": "Удобство",
                              "value": {
                                  "title": "Самое удобное удобство",
                              }
                          }})):
    fac = await db.facilities.add(data=data)
    await db.commit()
    return {"status": "OK", "data": fac}


