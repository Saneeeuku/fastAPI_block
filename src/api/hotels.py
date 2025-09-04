from fastapi import Query, Body, APIRouter
from sqlalchemy import insert, select

from src.models.hotels_model import HotelsOrm
from src.schemas.hotels_schemas import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_new_session, engine

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
        query = select(HotelsOrm)
        if location:
            query = query.filter(
                HotelsOrm.location.ilike(f"%{location}%")
                )
        if title:
            query = query.filter(
                HotelsOrm.title.ilike(f"%{title}%")
                )
        query = (
            query
            .limit(pagination.per_page)
            .offset((pagination.page - 1) * pagination.per_page)
         )
        result = await session.execute(query)
        _hotels = result.scalars().all()
    return _hotels


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = list(filter(lambda x: x['id'] != hotel_id, hotels))
    return {'status': 'OK'}


@router.post("/hotels", summary="Создание отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Чёрная жемчужина',
        'location': 'sochi'
        }
          },
    '2': {'summary': 'Дубай', 'value': {
        'title': 'Буржхалифа',
        'location': 'dubai'
        }
          }})):
    async with async_new_session() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'status': 'OK'}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
def change_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
            break
    else:
        return {'warning': 'Hotel not found.'}
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary="Изменение части информации отеля")
def change_hotel_partially(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            if hotel_data.name:
                hotel['name'] = hotel_data.name
            break
    else:
        return {'warning': 'Hotel not found.'}
    return {'status': 'OK'}
