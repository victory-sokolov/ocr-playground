from asyncio import current_task
from contextvars import ContextVar
from enum import Enum
from typing import AsyncIterator

from app.core.config import config
from sqlalchemy import Delete, Insert, Update
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

session_context: ContextVar[str] = ContextVar("session_context")


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


engines = {
    EngineType.WRITER: create_async_engine(
        config.WRITER_DB_URL,
        pool_recycle=3600,
        echo=config.SQLALCHEMY_ECHO,
    ),
    EngineType.READER: create_async_engine(
        config.READER_DB_URL,
        pool_recycle=3600,
        echo=config.SQLALCHEMY_ECHO,
    ),
}


class RoutingSession(Session):
    def get_bind(self, _mapper=None, clause=None, **_kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine

        return engines[EngineType.READER].sync_engine


class DatabaseSessionManager:
    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session = None
        self.session_maker = None

    def init_db(self):
        # Creating an asynchronous engine
        self.engine = create_async_engine(
            config.WRITER_DB_URL,
            max_overflow=0,
            pool_pre_ping=True,
            echo=config.SQLALCHEMY_ECHO,
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            class_=AsyncSession,
            sync_session_class=RoutingSession,
            expire_on_commit=False,
        )

        # Creating a scoped session
        self.session = async_scoped_session(
            session_factory=self.session_maker,
            scopefunc=current_task,
        )

    async def close(self):
        # Closing the database session...
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self.engine.dispose()


sessionmanager = DatabaseSessionManager()
sessionmanager.init_db()


async def get_db() -> AsyncIterator[AsyncSession]:
    session = sessionmanager.session()
    if session is None:
        raise Exception("DatabaseSessionManager is not initialized")
    try:
        yield session
    except Exception:
        await session.rollback()
    finally:
        await session.close()
