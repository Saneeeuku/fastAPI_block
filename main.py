import uvicorn
from fastapi import FastAPI, Query, Body, Form


app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Сочи', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'},
    ]


@app.get("/hotels")
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


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = list(filter(lambda x: x['id'] != hotel_id, hotels))
    return {'status': 'OK'}


@app.post("/hotels")
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


@app.put("/hotels/{hotel_id}")
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


@app.patch("/hotels/{hotel_id}")
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


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
