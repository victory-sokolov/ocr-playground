from models.document import Document
from schemas.document import DocumentSchema
from utils.repository import SQLAlchemyRepository


class DocumentRepository(SQLAlchemyRepository):
    model = Document

    async def create_document(self, content: dict) -> DocumentSchema:
        id = await self.add_one(content)
        response = await self.find_one(id)

        result = DocumentSchema.model_validate(response)
        json_result = result.json()
        return json_result
