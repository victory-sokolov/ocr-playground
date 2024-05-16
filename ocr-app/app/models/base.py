import uuid
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.db.mixins import TimestampMixin


class Base(DeclarativeBase, TimestampMixin):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
