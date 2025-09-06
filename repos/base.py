from pydantic import BaseModel
from sqlalchemy import select, insert, delete as sqla_delete, update
from sqlalchemy.exc import ArgumentError, NoResultFound, MultipleResultsFound
from fastapi import HTTPException


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_one(self, **filters):
        filters = {k: v for k, v in filters.items() if v is not None}
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        try:
            result = result.scalars().one()
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=e.args)
        except MultipleResultsFound as e:
            raise HTTPException(status_code=422, detail=e.args)
        return result

    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
         )
        # print(add_stmt.compile(compile_kwargs={"literal_binds": True}))
        res = await self.session.execute(add_stmt)
        return res.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset_and_none: bool = False, **filters):
        await self.get_one(**filters)
        upd_stmt = update(self.model).filter_by(**filters).values(
            **data.model_dump(exclude_unset=exclude_unset_and_none, exclude_none=exclude_unset_and_none))
        # print(upd_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(upd_stmt)

    async def delete(self, **filters):
        await self.get_one(**filters)
        del_stmt = sqla_delete(self.model).filter_by(**filters)
        # print(del_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(del_stmt)
