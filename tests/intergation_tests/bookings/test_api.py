import pytest
from pytest import mark


@pytest.fixture(scope="module")
async def clear_bookings_db(db):
    await db.bookings.delete()
    await db.commit()


@mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "01-08-2024", "10-08-2024", 200),
        (1, "01-08-2024", "10-08-2024", 200),
        (1, "01-08-2024", "10-08-2024", 200),
        (1, "01-08-2024", "10-08-2024", 200),
        (1, "01-08-2024", "10-08-2024", 200),
        (1, "01-08-2024", "10-08-2024", 422),
        (1, "11-08-2024", "12-08-2024", 200),
    ],
)
async def test_post_bookings(room_id, date_from, date_to, status_code, db, auth_ac):
    response = await auth_ac.post(
        "/bookings", json={"room_id": room_id, "date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "OK"
        assert res.get("data")


@mark.parametrize(
    "room_id, date_from, date_to, booking_count",
    [
        (1, "01-08-2024", "10-08-2024", 1),
        (1, "01-08-2024", "10-08-2024", 2),
        (1, "01-08-2024", "10-08-2024", 3),
    ],
)
async def test_post_and_get_users_bookings(
    room_id, date_from, date_to, booking_count, db, auth_ac, clear_bookings_db
):
    first_response = await auth_ac.post(
        "/bookings", json={"room_id": room_id, "date_from": date_from, "date_to": date_to}
    )
    assert first_response.status_code == 200

    user_id = first_response.json()["data"]["user_id"]

    second_response = await auth_ac.get("/bookings/me", params={"user_id": user_id})
    assert second_response.status_code == 200
    assert len(second_response.json()) == booking_count
