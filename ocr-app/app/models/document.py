from models.base import Base
from schemas.document import DocumentSchema
from sqlalchemy.orm import Mapped


class Document(Base):
    raw_data: Mapped[str]

    def to_read_model(self):
        return DocumentSchema(
            id=self.id,
            created_at=self.created_at,
            raw_data=self.raw_data,
        )
