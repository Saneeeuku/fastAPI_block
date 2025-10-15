from src.services.auth_service import AuthService


def test_create_access_toke():
    data = {"user_id": 1}
    token = AuthService().create_access_token(data=data)
    assert token
    assert isinstance(token, str)
