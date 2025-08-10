from pathlib import Path

from api import router as extract_views
from containers import RecognitionContainer
from core.config import config
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator
from utils.file import is_archive_file, save_file, unarchive_files

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=config.APP_NAME, debug=config.DEBUG)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(router=extract_views, prefix="/api/v1")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
async def _startup() -> None:
    instrumentator.expose(app)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse, include_in_schema=False)
async def upload_image(request: Request, file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only image files are supported.",
        )

    f_name = file.filename
    extension = f_name.split(".")[-1]
    logger.info(f"Uploading {f_name}", extra={"extension": extension})

    if extension not in config.ALLOWED_IMAGE_EXTENSIONS:
        return {"status": f"File with extension {extension} is not allowed"}

    save_file(file)
    processor = RecognitionContainer.processor()

    if not is_archive_file(extension):
        ocr = processor.process(f_name)
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "data": [ocr]},
        )

    files = unarchive_files(f_name)
    ocr = processor.process(files)
    return templates.TemplateResponse("result.html", {"request": request, "data": ocr})
