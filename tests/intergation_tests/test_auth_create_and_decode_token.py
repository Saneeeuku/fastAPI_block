from src.services.auth_service import AuthService


def test_create_access_toke():
    data = {"user_id": 1}
    token = AuthService().create_access_token(data)

    assert token
    assert isinstance(token, str)

    res = AuthService().decode_token(token)

    assert res
    assert res["user_id"] == data["user_id"]