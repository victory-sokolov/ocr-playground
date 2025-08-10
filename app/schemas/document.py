from pydantic import BaseModel

from .base import Base


class DocumentSchema(Base):
    raw_data: str


class OcrRequest(BaseModel):
    image_data: str
