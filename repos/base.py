from sqlalchemy import select, insert


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

    async def add(self, *args, **kwargs):
        add_stmt = insert(self.model).values(**kwargs)
        # print(add_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_stmt)
        res = add_stmt.compile().params
        return dict(res)
