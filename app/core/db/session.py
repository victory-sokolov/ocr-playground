from contextvars import ContextVar
from enum import Enum

from sqlalchemy import Delete, Insert, Update
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

from app.core.config import config

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


engines = {
    EngineType.WRITER: create_async_engine(
        config.WRITER_DB_URL, pool_recycle=3600, echo=config.SQLALCHEMY_ECHO,
    ),
    EngineType.READER: create_async_engine(
        config.READER_DB_URL, pool_recycle=3600, echo=config.SQLALCHEMY_ECHO,
    ),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine
        else:
            return engines[EngineType.READER].sync_engine


async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)
