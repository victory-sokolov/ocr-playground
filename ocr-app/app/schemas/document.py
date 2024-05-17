from models.base import Base
from sqlalchemy.orm import Mapped


class DocumentSchema(Base):
    raw_data: Mapped[str]

    class Config:
        from_attributes = True
