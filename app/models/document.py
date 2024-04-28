from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.schemas.document import DocumentSchema


class Document(Base):
    raw_data: Mapped[str] = mapped_column("raw_data", nullable=False, default="")

    def to_read_model(self):
        return DocumentSchema(
            id=self.id,
            created_at=self.created_at,
            raw_data=self.raw_data,
        )
