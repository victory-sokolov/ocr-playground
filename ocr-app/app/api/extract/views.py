from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.dependencies import document_service
from api.extract.schemas import OcrRequest, OcrResponse
from services.document import DocumentService

router = APIRouter(tags=["Optical Character Recognition"])


@router.post(
    "/",
    response_model=OcrResponse,
    status_code=status.HTTP_201_CREATED,
)
async def data_recognition(
    data: OcrRequest,
    service: Annotated[DocumentService, Depends(document_service)],
) -> Response:
    document = await service.create_document(data)
    return JSONResponse(content=jsonable_encoder(document))
