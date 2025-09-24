from datetime import date

from fastapi import Query, Body, APIRouter

from src.schemas.hotels_schemas import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="АДМИН_РУЧКА", description="Показывает все отели в таблице")
async def get_hotels(db: DBDep):
    return await db.hotels.get_all()


@router.get("/free", summary="Свободные отели",
            description="Показывает отели со свободными для бронирования номерами и с дополнительными параметрами")
async def get_free_hotels(
        db: DBDep,
        pagination: PaginationDep,
        date_from: date = Query(example="2024-08-01", description="Формат даты и разделитель менять нельзя"),
        date_to: date = Query(example="2024-08-10", description="Формат даты и разделитель менять нельзя"),
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
):
    return await db.hotels.get_by_time(date_from=date_from, date_to=date_to,
                                       title=title, location=location,
                                       limit=pagination.per_page, offset=(pagination.page - 1) * pagination.per_page)


@router.get("/{hotel_id}", summary="Отель", description="Получить отель по id")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one(id=hotel_id)


@router.post("/hotel", summary="Создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
        "1": {
        "summary": "Сочи",
        "value": {
            "title": "Чёрная жемчужина",
            "location": "sochi"
            }
            },
        "2": {
        "summary": "Дубай",
        "value": {
            "title": "Буржхалифа",
            "location": "dubai"
            }
            }
        })
):
    _hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "hotel": _hotel}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
async def change_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Изменение части информации отеля")
async def change_hotel_partially(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset_and_none=True)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(db: DBDep, hotel_id: int):
    db.hotels.delete(id=hotel_id)
    db.commit()
    return {"status": "OK"}


@router.delete("", summary="Удаление нескольких отелей", description="Используется частичное сравнение")
async def delete_few_hotels(
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация")
):
    await db.hotels.delete_few(title=title, location=location)
    await db.commit()
    return {"status": "OK"}
