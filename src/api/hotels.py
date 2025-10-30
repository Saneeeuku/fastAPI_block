from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import DateViolationException, ObjectNotFoundException
from src.schemas.hotels_schemas import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels_service import HotelsService

# from src.utils.self_cache_deco import my_cache

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="АДМИН_РУЧКА", description="Показывает все отели в таблице")
async def get_hotels(db: DBDep):
    return await HotelsService(db).get_hotels()


@router.get(
    "/free",
    summary="Свободные отели",
    description="Показывает отели со свободными для бронирования номерами и с дополнительными параметрами",
)
@cache(expire=10)
async def get_free_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(
        openapi_examples={"1": {"value": "2024-08-01"}},
        description="Формат даты и разделитель менять нельзя",
    ),
    date_to: date = Query(
        openapi_examples={"1": {"value": "2024-08-10"}},
        description="Формат даты и разделитель менять нельзя",
    ),
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация"),
):
    try:
        return await HotelsService(db).get_free_hotels(
            date_from, date_to, title, location, pagination
        )
    except DateViolationException as e:
        raise HTTPException(status_code=412, detail=e.detail)


@router.get("/{hotel_id}", summary="Отель", description="Получить отель по id")
# @my_cache(expire=10)
@cache(expire=10)
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")


@router.post("/hotel", summary="Создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {"summary": "Сочи", "value": {"title": "Чёрная жемчужина", "location": "sochi"}},
            "2": {"summary": "Дубай", "value": {"title": "Буржхалифа", "location": "dubai"}},
        }
    ),
):
    hotel = await HotelsService(db).create_hotel(hotel_data)
    return {"status": "OK", "hotel": hotel}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
async def change_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelsService(db).change_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Изменение части информации отеля")
async def change_hotel_partially(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelsService(db).change_hotel_partially(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.delete(
    "", summary="Удаление нескольких отелей", description="Используется частичное сравнение"
)
async def delete_few_hotels(
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация"),
):
    await HotelsService(db).delete_few_hotels(title, location)
    return {"status": "OK"}
