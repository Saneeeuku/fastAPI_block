from typing import cast

from sqlalchemy import select, or_, delete, insert, and_, literal

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
        room_current_fac = (
            select(RoomsFacilitiesOrm.facility_id)
            .select_from(RoomsFacilitiesOrm)
            .filter_by(room_id=room_id)
            .cte(name="room_current_fac")
        )
        # print(room_current_fac.compile(compile_kwargs={"literal_binds": True}))
        # print("*" * 20, end='\n')

        new_fac = (
            select(FacilitiesOrm.id)
            .filter(or_(FacilitiesOrm.id == el for el in facilities_ids))
            .cte(name="new_fac")
        )
        # print(new_fac.compile(compile_kwargs={"literal_binds": True}))
        # print("*"*20, end='\n')

        fac_to_delete = (
            select(room_current_fac.c.facility_id)
            .select_from(room_current_fac)
            .outerjoin(new_fac, cast("ColumnElement[bool]", room_current_fac.c.facility_id == new_fac.c.id))
            .where(new_fac.c.id.is_(None))
        )
        # print(fac_to_delete.compile(compile_kwargs={"literal_binds": True}))
        # print("*" * 20, end='\n')
        delete_fac = (
            delete(RoomsFacilitiesOrm)
            .filter_by(room_id=room_id)
            .filter(RoomsFacilitiesOrm.facility_id.in_(fac_to_delete))
        )
        await self.session.execute(delete_fac)
        # print(delete_fac.compile(compile_kwargs={"literal_binds": True}))
        # print("*" * 20, end='\n')
        fac_to_add = (
            select(new_fac.c.id.label("facility_id"), literal(room_id).label("room_id"))
            .select_from(new_fac)
            .outerjoin(room_current_fac, cast("ColumnElement[bool]", new_fac.c.id == room_current_fac.c.facility_id))
            .where(and_(
                room_current_fac.c.facility_id.is_(None))
            )
            .cte("fac_to_add")
        )
        # print(fac_to_add.compile(compile_kwargs={"literal_binds": True}))
        # print("*" * 20, end='\n')
        add_fac = (
            insert(RoomsFacilitiesOrm)
            .from_select(["facility_id", "room_id"], select(fac_to_add))
        )
        print(add_fac.compile(compile_kwargs={"literal_binds": True}))
        print("*" * 20, end='\n')
        await self.session.execute(add_fac)
