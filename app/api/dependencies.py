from app.repositories.document import DocumentRepository
from app.services.document import DocumentService


def document_service():
    return DocumentService(DocumentRepository)
