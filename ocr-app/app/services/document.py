from containers import RecognitionContainer
from repositories.document import DocumentRepository
from schemas.document import DocumentSchema, OcrRequest


class DocumentService:
    def __init__(self, document_repo: DocumentRepository) -> None:
        self.repository = document_repo()

    async def create_document(self, data: OcrRequest) -> DocumentSchema:
        processor = RecognitionContainer.processor()
        ocr_data = processor.process(data.get("image_data", ""))
        content = {"raw_data": ocr_data["text"]}
        response = await self.repository.create_document(content)
        return response
