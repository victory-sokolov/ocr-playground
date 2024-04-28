from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.extract.schemas import OcrRequest, OcrResponse
from app.containers import RecognitionContainer
from app.core.db.session import get_db
from app.repositories.document import DocumentRepository

router = APIRouter(tags=["Optical Character Recognition"])


@router.post(
    "/",
    response_model=OcrResponse,
    status_code=status.HTTP_201_CREATED,
)
async def data_recognition(
    data: OcrRequest,
    db: AsyncSession = Depends(get_db),
) -> Response:
    processor = RecognitionContainer.processor()
    ocr_data = processor.process(data.image_data)
    content = {"raw_data": ocr_data}
    repository = DocumentRepository(db)
    id = await repository.add_one(content)
    response = await repository.find_one(id)
    return JSONResponse(content=jsonable_encoder(response))
