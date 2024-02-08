from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.extract.schemas import OcrRequest, OcrResponse
from app.containers import RecognitionContainer

router = APIRouter(tags=["Optical Character Recognition"])


@router.post(
    "/",
    response_model=OcrResponse,
    status_code=status.HTTP_201_CREATED,
)
async def ocr(data: OcrRequest):
    processor = RecognitionContainer.processor()
    ocr_data = processor.process(data.image_data)
    return JSONResponse(content={"data": ocr_data})
