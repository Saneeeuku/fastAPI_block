from fastapi import Query, Body, Form, APIRouter


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1, 'title': 'Сочи', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'},
    ]


@router.get("",
         summary="Отели",
         description="Показывает все отели или по заданным параметрам")
def get_hotels(
        id: int | None = Query(None, description='Айди'),
        title: str | None = Query(None, description='Название отеля')
        ):
    _hotels = []
    for hotel in hotels:
        if id and id != hotel['id']:
            continue
        if title and title != hotel['title']:
            continue
        _hotels.append(hotel)
    return _hotels


@router.delete("/{hotel_id}", summary="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = list(filter(lambda x: x['id'] != hotel_id, hotels))
    return {'status': 'OK'}


@router.post("/hotels", summary="Создание отеля")
def create_hotel(
        title: str = Body(),
        name: str = Body()
        ):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title,
        'name': name
        })
    return {'status': 'OK'}


@router.put("/{hotel_id}", summary="Изменение всех данных отеля")
def change_hotel(
        hotel_id: int,
        title: str = Form(...),
        name: str = Form(...)
        ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
            break
    else:
        return {'warning': 'Hotel not found.'}
    return {'status': 'OK'}


@router.patch("/{hotel_id}", summary="Изменение части информации отеля")
def change_hotel_partially(
        hotel_id: int,
        title: str | None = Form(None),
        name: str | None = Form(None)
        ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if title:
                hotel['title'] = title
            if name:
                hotel['name'] = name
            break
    else:
        return {'warning': 'Hotel not found.'}
    return {'status': 'OK'}
