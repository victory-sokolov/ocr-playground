from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", include_in_schema=False)
def health(_request: Request):
    return JSONResponse(content={"status": "ok"})
