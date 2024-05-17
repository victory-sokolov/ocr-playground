from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import insert, select

from core.db.session import get_db
from models.base import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: UUID):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = Base

    def __init__(self) -> None:
        self.async_session = get_db()

    async def add_one(self, data: dict) -> UUID:
        async for db_session in get_db():
            async with db_session as session:
                stmt = insert(self.model).values(**data).returning(self.model.id)
                res = await session.execute(stmt)
                await session.commit()
        return res.scalar_one()

    async def find_all(self):
        async for db_session in get_db():
            async with db_session as session:
                stmt = select(self.model)
                res = await session.execute(stmt)
                res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, id: UUID):
        async for db_session in get_db():
            async with db_session as session:
                stmt = select(self.model).filter_by(id=id)
                res = await session.execute(stmt)
                data = res.fetchone()
                if not data:
                    raise HTTPException(status_code=404, detail="Item not found")
        return data[0].to_read_model()
