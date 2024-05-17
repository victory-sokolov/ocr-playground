from models.base import Base
from schemas.document import DocumentSchema
from sqlalchemy.orm import Mapped, mapped_column


class Document(Base):
    raw_data: Mapped[str] = mapped_column("raw_data", nullable=False, default="")

    def to_read_model(self):
        return DocumentSchema(
            id=self.id,
            created_at=self.created_at,
            raw_data=self.raw_data,
        )
