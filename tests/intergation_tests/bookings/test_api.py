async def test_post_bookings(db, auth_ac):
    room_id = (await db.rooms.get_all())[0].id
    data = {
        "room_id": room_id,
        "date_from": "01-08-2024",
        "date_to": "10-08-2024"
    }
    response = await auth_ac.post(
        "/bookings",
        json=data
    )
    assert response.status_code == 200

    res = response.json()
    assert res["status"] == "OK"
    assert res.get("data")
    print(res.get("data"))
