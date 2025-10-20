

async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200


async def test_post_facilities(ac):
    data = {"title": "Удобство"}
    response = await ac.post(
        "/facilities",
        json=data
    )
    data_title = response.json().get("data")["title"]

    assert response.status_code == 200 and data_title == data["title"]


