from fastapi import Query, Body, APIRouter

from src.schemas.hotels_schemas import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1, 'title': 'Сочи', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
    ]


@router.get("",
         summary="Отели",
         description="Показывает все отели или по заданным параметрам")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description='Айди'),
    title: str | None = Query(None, description='Название отеля'),
    ):
    _hotels = []
    for hotel in hotels:
        if id and id != hotel['id']:
            continue
        if title and title != hotel['title']:
            continue
        _hotels.append(hotel)
    return _hotels[((pagination.page - 1) * pagination.per_page):pagination.page * pagination.per_page]


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = list(filter(lambda x: x['id'] != hotel_id, hotels))
    return {'status': 'OK'}


@router.post("/hotels", summary="Создание отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Отель у моря 5 звёзд',
        'name': 'sochi_seaside'
        }
    },
    '2': {'summary': 'Дубай', 'value': {
        'title': 'Отель Дубай Бурджхалифа',
        'name': 'dubai_burjhalifa'
        }
    }
})):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
        })
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
