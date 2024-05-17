from repositories.document import DocumentRepository
from services.document import DocumentService


def document_service():
    return DocumentService(DocumentRepository)
