from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from app.config import config
from app.containers import RecognitionContainer
from app.utils.file import is_archive_file, save_file, unarchive_files

Config = config["development"]
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
def upload_image(request: Request, file: UploadFile = File(...)):
    f_name = file.filename
    extension = f_name.split(".")[-1]
    logger.info(f"Uploading {f_name}", extra={"extension": extension})

    if extension not in Config.ALLOWED_IMAGE_EXTENSIONS:
        return {"status": f"File with extension {extension} is not allowed"}

    save_file(file)
    processor = RecognitionContainer.processor()

    if not is_archive_file(extension):
        ocr = processor.process(f_name)
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "data": ocr},
        )

    files = unarchive_files(f_name)
    ocr = processor.process(files)
    return templates.TemplateResponse("result.html", {"request": request, "data": ocr})
