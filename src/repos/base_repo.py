from pydantic import BaseModel
from sqlalchemy import select, insert, delete as sqla_delete, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from fastapi import HTTPException


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        """Takes session object"""
        self.session = session

    async def get_filtered(self, *q_filter, **filters):
        query = (
            select(self.model)
            .filter(*q_filter)
            .filter_by(**filters)
        )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        if result:
            result = self.schema.model_validate(result, from_attributes=True)
        return result

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
        return self.schema.model_validate(result, from_attributes=True)

    async def add(self, data: BaseModel):
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
            )
        # print(add_stmt.compile(compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError as e:
            raise HTTPException(status_code=422, detail=f"{e.__class__.__name__}: {e.orig.args[0].split('DETAIL:  ')[1]}")
        result = result.scalars().one()
        return self.schema.model_validate(result, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_stmt = insert(self.model).values([el.model_dump() for el in data])
        try:
            await self.session.execute(add_stmt)
        except IntegrityError as e:
            raise HTTPException(status_code=422, detail=f"{e.__class__.__name__}: {e.orig.args[0].split('DETAIL:  ')[1]}")

    async def edit(self, data: BaseModel, exclude_unset_and_none: bool = False, **filters):
        await self.get_one(**filters)
        upd_stmt = update(self.model).filter_by(**filters).values(
            **data.model_dump(exclude_unset=exclude_unset_and_none, exclude_none=exclude_unset_and_none))
        # print(upd_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(upd_stmt)

    async def delete(self, *q_filter, **filters):
        await self.get_one(**filters)
        del_stmt = (
            sqla_delete(self.model)
            .filter(*q_filter)
            .filter_by(**filters)
        )
        # print(del_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(del_stmt)
