from typing import cast

from fastapi import HTTPException
from sqlalchemy import select, or_, delete, insert, literal
from sqlalchemy.exc import SQLAlchemyError

from src.models.facilities_model import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base_repo import BaseRepository
from src.schemas.facilities_schemas import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def change_facilities(self, room_id: int, facilities_ids: list[int]):
        try:
            room_current_fac = (
                select(RoomsFacilitiesOrm.facility_id)
                .select_from(RoomsFacilitiesOrm)
                .filter_by(room_id=room_id)
                .cte(name="room_current_fac")
            )

            new_fac = (
                select(FacilitiesOrm.id)
                .filter(or_(FacilitiesOrm.id == el for el in facilities_ids))
                .cte(name="new_fac")
            )
        except AssertionError:
            raise HTTPException(status_code=422, detail="Возникла ошибка с изменением данных")

        fac_to_delete = (
            select(room_current_fac.c.facility_id)
            .select_from(room_current_fac)
            .outerjoin(new_fac, cast("ColumnElement[bool]", room_current_fac.c.facility_id == new_fac.c.id))
            .where(new_fac.c.id.is_(None))
        )

        try:
            delete_fac = (
                delete(RoomsFacilitiesOrm)
                .filter_by(room_id=room_id)
                .filter(RoomsFacilitiesOrm.facility_id.in_(fac_to_delete))
            )
            await self.session.execute(delete_fac)
            # print(delete_fac.compile(compile_kwargs={"literal_binds": True}))
            # print("*" * 20, end='\n')
        except SQLAlchemyError:
            raise Exception("Возникла ошибка с изменением данных")

        fac_to_add = (
            select(new_fac.c.id.label("facility_id"), literal(room_id).label("room_id"))
            .select_from(new_fac)
            .outerjoin(room_current_fac, cast("ColumnElement[bool]", new_fac.c.id == room_current_fac.c.facility_id))
            .where(room_current_fac.c.facility_id.is_(None))
            .cte("fac_to_add")
        )

        try:
            add_fac = (
                insert(RoomsFacilitiesOrm)
                .from_select(["facility_id", "room_id"], select(fac_to_add))
            )
            # print(add_fac.compile(compile_kwargs={"literal_binds": True}))
            # print("*" * 20, end='\n')
            await self.session.execute(add_fac)
        except SQLAlchemyError:
            raise Exception("Возникла ошибка с изменением данных")
