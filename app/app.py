import shutil
from os import getcwd, listdir
from os.path import isfile, join

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from app.config import config
from app.containers import RecognitionContainer
from app.utils.file import is_archive_file, save_file
from app.utils.helpers import clean

Config = config["development"]
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ocr-results", response_class=HTMLResponse)
def ocr_result(request: Request):
    nums = {"image": "static/IDCardDataSet/document_1.jpg"}
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "results": nums},
    )


@app.post("/upload", response_class=HTMLResponse)
def upload_image(request: Request, file: UploadFile = File(...)):
    f_name = file.filename
    logger.info(f"Uploading {f_name}")
    extension = f_name.split(".")[-1]
    processor = RecognitionContainer.processor()

    if extension not in Config.ALLOWED_IMAGE_EXTENSIONS:
        return {"status": f"File with extension {extension} is not allowed"}

    save_file(file)
    if not is_archive_file(extension):
        ocr = processor.process(f_name)
        # ocr = clean(ocr)
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "data": ocr},
        )

    # Handling archived files
    logger.info("Archiving files...")
    folder = f"{f_name.split('.')[0]}/"
    # file path where to extract archive images
    file_path = f"static/{folder}"
    shutil.unpack_archive(f"{getcwd()}/static/images/{f_name}", file_path)
    files = [folder + f for f in listdir(file_path) if isfile(join(file_path, f))]

    ocr = processor.process(files)
    ocr = clean(ocr)
    return templates.TemplateResponse("result.html", {"request": request, "data": ocr})
