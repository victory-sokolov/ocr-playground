from sqlalchemy.orm import Mapped

from app.models.base import Base


class DocumentSchema(Base):
    raw_data: Mapped[str]

    class Config:
        from_attributes = True
