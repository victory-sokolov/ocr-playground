from app.models.document import Document
from app.utils.repository import SQLAlchemyRepository


class DocumentRepository(SQLAlchemyRepository):
    model = Document
