from fastapi import Query, Body, APIRouter

from src.repos.hotels_repo import HotelsRepository
from src.schemas.hotels_schemas import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_new_session

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("",
            summary="Отели",
            description="Показывает все отели или по заданным параметрам")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Локация'),
        ):

    async with async_new_session() as session:
        return await HotelsRepository(session).get_all(
            location=location, title=title, limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page)


@router.get("/{hotel_id}",
            summary="Отель",
            description="Получить отель по id")
async def get_hotel(hotel_id: int):
    async with async_new_session() as session:
        return await HotelsRepository(session).get_one(id=hotel_id)


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
async def delete_hotel(hotel_id: int):
    async with async_new_session() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete("", summary="Удаление нескольких отелей", description="Используется частичное сравнение")
async def delete_few_hotels(
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Локация')
        ):
    async with async_new_session() as session:
        await HotelsRepository(session).delete_few(title=title, location=location)
        await session.commit()
    return {'status': 'OK'}


@router.post("/hotel", summary="Создание отеля")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
        '1': {
        'summary': 'Сочи',
        'value': {
            'title': 'Чёрная жемчужина',
            'location': 'sochi'
            }
            },
        '2': {
        'summary': 'Дубай',
        'value': {
            'title': 'Буржхалифа',
            'location': 'dubai'
            }
            }
        })):
    async with async_new_session() as session:
        _hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {'status': 'OK', 'hotel': _hotel}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
async def change_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_new_session() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary="Изменение части информации отеля")
async def change_hotel_partially(hotel_id: int, hotel_data: HotelPATCH):
    async with async_new_session() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset_and_none=True)
        await session.commit()
    return {'status': 'OK'}
