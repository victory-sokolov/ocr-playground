import asyncio

from api.dependencies import document_service
from celery import Task
from schemas.document import OcrRequest
from worker import app


class RecognitionTask(Task):
    name = "RecognitionTask"

    def run(self, data: OcrRequest):
        service = document_service()
        document = asyncio.run(service.create_document(data))
        return document


app.register_task(RecognitionTask())
