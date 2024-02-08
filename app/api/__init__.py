from fastapi import APIRouter

from .extract.views import router as extract_views

router = APIRouter()
router.include_router(router=extract_views, prefix="/ocr")
