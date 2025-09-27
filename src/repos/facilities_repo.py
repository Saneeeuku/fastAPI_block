from typing import cast

from fastapi import HTTPException
from sqlalchemy import select, or_, delete, insert, literal
from sqlalchemy.exc import SQLAlchemyError

from src.models.facilities_model import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base_repo import BaseRepository
from src.repos.mappers.mappers import RoomFacilitiesDataMapper, FacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilitiesDataMapper

    async def change_facilities(self, room_id: int, facilities_ids: list[int]):
        if not facilities_ids:
            await self.session.execute(delete(self.model).filter_by(room_id=room_id))
            return
        room_current_fac = (
            select(RoomsFacilitiesOrm.facility_id)
            .select_from(RoomsFacilitiesOrm)
            .filter_by(room_id=room_id)
            .cte(name="room_current_fac")
        )
        try:
            new_fac = (
                select(FacilitiesOrm.id)
                .filter(or_(FacilitiesOrm.id == el for el in facilities_ids))
                .cte(name="new_fac")
            )
        except AssertionError as e:
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

    # async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
    #  """более эффективный код"""
    #     get_current_facilities_ids_query = (
    #         select(self.model.facility_id)
    #         .filter_by(room_id=room_id)
    #     )
    #     res = await self.session.execute(get_current_facilities_ids_query)
    #     current_facilities_ids: list[int] = res.scalars().all()
    #     ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))
    #     ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))
    #
    #     if ids_to_delete:
    #         delete_m2m_facilities_stmt = (
    #             delete(self.model)
    #             .filter(
    #                 self.model.room_id == room_id,
    #                 self.model.facility_id.in_(ids_to_delete),
    #             )
    #         )
    #         await self.session.execute(delete_m2m_facilities_stmt)
    #
    #     if ids_to_insert:
    #         insert_m2m_facilities_stmt = (
    #             insert(self.model)
    #             .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
    #         )
    #         await self.session.execute(insert_m2m_facilities_stmt)
