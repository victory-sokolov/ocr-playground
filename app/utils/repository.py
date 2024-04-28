from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


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

    def __init__(self, db: AsyncSession) -> None:
        self.session = db

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, id: UUID):
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        data = res.fetchone()
        if not data:
            return None
        return data[0].to_read_model()
