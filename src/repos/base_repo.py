import logging

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, delete as sqla_delete, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError

from src.exceptions import ObjectNotFoundException, DataConflictException
from src.repos.mappers.base_mapper import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        """Takes session object"""
        self.session = session

    async def get_filtered(self, *q_filter, **filters):
        query = select(self.model).filter(*q_filter).filter_by(**filters)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        if result:
            result = self.mapper.map_to_domain_entity(result)
        return result

    async def get_one(self, **filters):
        filters = {k: v for k, v in filters.items() if v is not None}
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        try:
            result = result.scalars().one()
        except (NoResultFound, MultipleResultsFound):
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(result)

    async def get_one_from_query_result(self, query_result):
        try:
            result = query_result.scalars().one()
        except (NoResultFound, MultipleResultsFound):
            raise ObjectNotFoundException
        return result

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(add_stmt)
        except IntegrityError as e:
            logging.error(
                f"Не удалось добавить данные в базу данных ({data=}, ошибка {type(e.orig.__cause__)=})"
            )
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise DataConflictException from e
            else:
                logging.error(f"Неизвестная ошибка ({data=}, ошибка {type(e.orig.__cause__)=})")
                raise e
        result = result.scalars().one()
        return self.mapper.map_to_domain_entity(result)

    async def add_bulk(self, data: list[BaseModel]):
        add_stmt = insert(self.model).values([el.model_dump() for el in data])
        try:
            await self.session.execute(add_stmt)
        except IntegrityError:
            raise DataConflictException

    async def edit(self, data: BaseModel, exclude_unset_and_none: bool = False, **filters):
        try:
            await self.get_one(**filters)
        except ObjectNotFoundException as e:
            raise e
        upd_stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(
                **data.model_dump(
                    exclude_unset=exclude_unset_and_none, exclude_none=exclude_unset_and_none
                )
            )
        )
        await self.session.execute(upd_stmt)

    async def delete(self, *q_filter, **filters):
        if filters:
            try:
                await self.get_one(**filters)
            except ObjectNotFoundException as e:
                raise e
        del_stmt = sqla_delete(self.model).filter(*q_filter).filter_by(**filters)
        await self.session.execute(del_stmt)
