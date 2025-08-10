from abc import ABC, abstractmethod
from typing import NoReturn
from uuid import UUID

from core.db.session import get_db
from fastapi import HTTPException
from models.base import Base
from sqlalchemy import insert, select


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: UUID) -> NoReturn:
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
                session.refresh(res)
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
                data = res.scalar_one()
                if not data:
                    raise HTTPException(status_code=404, detail="Item not found")
        return data
