import json

from api.tasks import RecognitionTask
from fastapi import APIRouter, Response, status
from fastapi.encoders import jsonable_encoder
from schemas.document import OcrRequest

router = APIRouter(tags=["Optical Character Recognition"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def data_recognition(
    data: OcrRequest,
) -> Response:
    json_data = jsonable_encoder(data)
    document = RecognitionTask().apply_async(args=(json_data,))
    result = document.get()
    return jsonable_encoder(json.loads(result))
