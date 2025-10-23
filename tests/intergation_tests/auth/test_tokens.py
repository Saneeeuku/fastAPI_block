from src.services.auth_service import AuthService


def test_create_access_token():
    data = {"id": 1, "nickname": "qwerty"}
    token = AuthService().create_access_token(data)

    assert token
    assert isinstance(token, str)

    res = AuthService().decode_token(token)

    assert res
    assert res["id"] == data["id"] and res["nickname"] == data["nickname"]
