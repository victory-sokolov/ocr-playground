import json
import shutil
from os import getcwd, listdir
from os.path import isfile, join

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import config
from detect_mrz import get_mrz
from Recognition import Recogniser
from utils.file import is_archive_file, save_file

config_name = config['development']
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/result', response_class=HTMLResponse)
def ocr_result(request: Request):
    nums = {"image": "static/IDCardDataSet/document_1.jpg"}
    return templates.TemplateResponse("result.html", {"request": request, "results": nums})


@app.post('/upload')
def upload_image(file: UploadFile = File(...)):
    f = file.filename
    recogniser = Recogniser()

    if f.endswith(tuple(config_name.ALLOWED_IMAGE_EXTENSIONS)):
        save_file(file)
        if is_archive_file(f):
            folder = f"{f.split('.')[0]}/"
            # file path where to extract archive images
            file_path = f'static/{folder}'
            shutil.unpack_archive(f'{getcwd()}/static/{f}', file_path)
            files = [
                folder + f
                for f in listdir(file_path)
                if isfile(join(file_path, f))
            ]

            ocr = recogniser.recognise(files)
            ocr = clean(ocr)
            return ocr

        result = recogniser.recognise(f)
        data = clean(result)

        return {'data': data}, 200

    return {'Status': 'File not allowed'}


def clean(txt_data):
    result_data = txt_data
    for index, txt in enumerate(txt_data):
        data = " ".join(txt['ocr'].split())
        result_data[index]['ocr'] = data

    return result_data
