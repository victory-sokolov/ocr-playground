from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Base(BaseModel):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
