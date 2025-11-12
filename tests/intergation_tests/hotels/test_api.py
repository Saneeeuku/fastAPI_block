from datetime import date, timedelta

async def test_get_hotels(ac):
    date_from = date.today()
    date_to = date_from + timedelta(days=1)

    data = {
        "date_from": date_from,
        "date_to": date_to,
    }
    response = await ac.get("/hotels/free", params=data)
    assert response.status_code == 200
