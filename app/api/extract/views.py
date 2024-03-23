from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from app.api.extract.schemas import OcrRequest, OcrResponse
from app.containers import RecognitionContainer

router = APIRouter(tags=["Optical Character Recognition"])


@router.post(
    "/",
    response_model=OcrResponse,
    status_code=status.HTTP_201_CREATED,
)
async def data_recognition(data: OcrRequest) -> Response:
    processor = RecognitionContainer.processor()
    ocr_data = processor.process(data.image_data)
    return JSONResponse(content={"raw_data": ocr_data})
