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

    async def edit(self, data: BaseModel, **filters):
        await self.get_one(**filters)
        upd_query = update(self.model).filter_by(**filters).values(**data.model_dump())
        print(upd_query.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(upd_query)

    async def delete(self, **filters):
        await self.get_one(**filters)
        del_query = sqla_delete(self.model).filter_by(**filters)
        # print(del_query.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(del_query)
