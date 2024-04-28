from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Mapped


class Base(BaseModel):
    id: UUID
    created_at: Mapped[datetime]

    class Config:
        from_attributes = True
