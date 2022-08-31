from os import getcwd, listdir
from os.path import isfile, join
import shutil
from config import config
from containers import RecognitionContainer
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils.helpers import clean
from utils.file import is_archive_file, save_file

from loguru import logger


config_name = config["development"]
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
        "result.html", {"request": request, "results": nums}
    )


@app.post("/upload", response_class=HTMLResponse)
def upload_image(request: Request, file: UploadFile = File(...)):
    f = file.filename
    logger.info(f"Uploading {f}")
    extension = f.split(".")[-1]
    processor = RecognitionContainer.processor()

    if extension in config_name.ALLOWED_IMAGE_EXTENSIONS:
        save_file(file)
        if is_archive_file(extension):
            logger.info("Unarchiving files...")
            folder = f"{f.split('.')[0]}/"
            # file path where to extract archive images
            file_path = f"static/{folder}"
            shutil.unpack_archive(f"{getcwd()}/static/images/{f}", file_path)
            files = [
                folder + f for f in listdir(file_path) if isfile(join(file_path, f))
            ]

            ocr = processor.process(files)
            ocr = clean(ocr)
            return templates.TemplateResponse(
                "result.html", {"request": request, "data": ocr}
            )

        ocr = processor.process(f)
        # ocr = clean(ocr)
        return templates.TemplateResponse(
            "result.html", {"request": request, "data": ocr}
        )

    return {"status": f"File with extension {extension} is not allowed"}
