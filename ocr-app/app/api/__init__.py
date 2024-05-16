from fastapi import APIRouter

from .extract.views import router as extract_views
from .health import router as health

router = APIRouter()
router.include_router(router=extract_views, prefix="/ocr")
router.include_router(router=health)
