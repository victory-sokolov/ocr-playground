from models.document import Document
from schemas.document import DocumentSchema
from utils.repository import SQLAlchemyRepository


class DocumentRepository(SQLAlchemyRepository):
    model = Document

    async def get_document_data(self, content: dict) -> DocumentSchema:
        id = await self.add_one(content)
        response = await self.find_one(id)
        return response