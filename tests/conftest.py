import json
from collections.abc import AsyncIterable
from mocks import *

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool, async_new_session_null_pool
from src.models import *
from src.schemas.hotels_schemas import HotelAdd
from src.schemas.rooms_schemas import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncIterable:
    async with DBManager(session_factory=async_new_session_null_pool) as db:
        yield db


@pytest.fixture()
async def db(check_test_mode) -> DBManager:
    app.dependency_overrides[get_db] = get_db_null_pool
    async for db in get_db_null_pool():
        yield db



@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    hotels_data = receive_data_from_json("mock_hotels.json")
    rooms_data = receive_data_from_json("mock_rooms.json")

    async with DBManager(session_factory=async_new_session_null_pool) as db:
        await db.hotels.add_bulk([HotelAdd.model_validate(h) for h in hotels_data])
        await db.rooms.add_bulk([RoomAdd.model_validate(r) for r in rooms_data])
        await db.commit()


@pytest.fixture(scope="session")
async def ac(check_test_mode) -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def create_user(setup_db, ac) -> None:
    data = {
            "email": "qwerty@mail.com",
            "password": "strongpassword",
            "nickname": "coolnickname"
        }
    await ac.post(
        "/auth/registration",
        json=data
    )


@pytest.fixture(scope="session")
async def auth_ac(create_user, ac) -> AsyncClient:
    data = {
        "email": "qwerty@mail.com",
        "password": "strongpassword"}
    response = await ac.post(
        "/auth/login",
        json=data
    )
    assert response.cookies.get("access_token")
    yield ac


def receive_data_from_json(json_filename: str) -> list[dict]:
    """Json files should be placed in tests folder
    :arg str json_filename: name with extension
    """
    with open(f"./tests/{json_filename}", mode="r", encoding='utf-8') as f:
        file = json.load(f)
    return file
