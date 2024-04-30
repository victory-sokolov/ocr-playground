from app.api.extract.schemas import OcrRequest
from app.containers import RecognitionContainer
from app.repositories.document import DocumentRepository
from app.schemas.document import DocumentSchema


class DocumentService:
    def __init__(self, document_repo: DocumentRepository):
        self.repository = document_repo()

    async def create_document(self, data: OcrRequest) -> DocumentSchema:
        processor = RecognitionContainer.processor()
        ocr_data = processor.process(data.image_data)
        content = {"raw_data": ocr_data}
        response = await self.repository.get_document_data(content)
        return response
