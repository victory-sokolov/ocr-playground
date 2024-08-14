from repositories.document import DocumentRepository
from services.document import DocumentService


def document_service() -> DocumentService:
    return DocumentService(DocumentRepository)
