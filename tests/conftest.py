import json
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert

from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *


@pytest.fixture(autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(autouse=True)
async def setup_db(check_test_mode) -> None:
    hotels_data = receive_data_from_json("mock_hotels")
    rooms_data = receive_data_from_json("mock_rooms")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(insert(HotelsOrm).values(hotels_data))
        await conn.execute(insert(RoomsOrm).values(rooms_data))


@pytest.fixture(autouse=True)
async def create_user(setup_db) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/registration",
            json={
                "email": "qwerty@mail.com",
                "password": "strongpassword",
                "nickname": "coolnickname"
            }
        )


def receive_data_from_json(json_filename: str) -> list[dict]:
    """Json files should be placed in project root folder
    :arg str json_filename: name without extension
    """
    full_path_to_json = _paths_to_json_file(json_filename)
    with open(full_path_to_json, mode="r", encoding='utf-8') as f:
        file = json.load(f)
    return file


def _paths_to_json_file(json_filename: str):
    project_root_name = "fastAPI_block"
    root_path = Path(__file__)
    while root_path.name != project_root_name:
        root_path = root_path.parent
    return root_path.joinpath(f"./{json_filename}.json")
