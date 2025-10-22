from pytest import mark


@mark.parametrize("email, password, nickname, status_code", [
    ("qwerty@mail.com", "strongpassword", "coolnickname", 422),
    ("qwerty1@mail.com", "strongpassword", "coolnickname", 422),
    ("qwerty1@mail.com", "strongpassword", "coolnickname1", 200),
    ("qwerty2@mail.com", "strongpassword", "coolnickname2", 200),
    ("qwerty2@", "strongpassword", "coolnickname3", 422),
])
async def test_post_register(
    email, password, nickname, status_code,
    ac, db
):
    response = await ac.post(
        "/auth/registration",
        json={
            "email": email,
            "password": password,
            "nickname": nickname
        }
    )
    assert response.status_code == status_code


@mark.parametrize("user_id, email, password, status_code", [
    (1, "qwe@mail.com", "111", 404),
    (1, "qwe@", "111", 422),
    (1, "qwerty@mail.com", "strongpassword", 200),
    (1, "qwerty@mail.com", "strongpassword1", 401),
    (4, "qwerty1@mail.com", "strongpassword", 200),
    (5, "qwerty2@mail.com", "strongpassword2", 401),
    (5, "qwerty2@mail.com", "strongpassword", 200),
])
async def test_login_and_me_and_delete(
    user_id, email, password, status_code,
    ac, db
):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        assert response.cookies.get("access_token")

        resp_me_after_login = await ac.get("/auth/me")
        assert resp_me_after_login.json().get("id") == user_id
        assert resp_me_after_login.json().get("email") == email

        resp_logout = await ac.delete("/auth/logout")
        assert resp_logout.json().get("status") == "OK"
        assert resp_logout.cookies.get("access_token") is None

    resp_me_not_login = await ac.get("/auth/me")
    assert resp_me_not_login.status_code == 401
    assert resp_me_not_login.json().get("detail") == "Отсутствует токен авторизации"
