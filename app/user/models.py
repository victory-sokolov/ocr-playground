from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.mixins import TimestampMixin
from app.core.db import Base


class User(Base, TimestampMixin):
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
