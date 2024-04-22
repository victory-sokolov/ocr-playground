from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.core.db.base import Base
from app.core.db.mixins import TimestampMixin


class Document(Base, TimestampMixin):
    raw_data: Mapped[str] = mapped_column(
        nullable=False,
    )
