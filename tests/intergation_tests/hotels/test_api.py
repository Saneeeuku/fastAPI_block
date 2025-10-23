async def test_get_hotels(ac):
    data = {
        "date_from": "2024-08-01",
        "date_to": "2024-08-10",
    }
    response = await ac.get("/hotels/free", params=data)
    assert response.status_code == 200
