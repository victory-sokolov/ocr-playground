import shutil
from os import getcwd, listdir
from os.path import isfile, join

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import config
from detect_mrz import get_mrz
from Recognition import Recogniser
from utils.file import is_archive_file, save_file

config_name = config['development']
app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/upload')
def upload_image(file: UploadFile = File(...)):
    f = file.filename

    if f.endswith(tuple(config_name.ALLOWED_IMAGE_EXTENSIONS)):
        save_file(file)
        if is_archive_file(f):
            folder = f"static/{f.split('.')[0]}"
            shutil.unpack_archive(f'{getcwd()}/static/{f}', folder)
            files = [f for f in listdir(folder) if isfile(join(folder, f))]

            mrz = get_mrz(files)
            # recogniser = Recogniser('eng', mrz)
            # data = recogniser.recognise()
            return {'Status': 'Ok'}, 200

        mrz = get_mrz(f)
        recogniser = Recogniser('eng', mrz)
        data = recogniser.recognise()
        return {'data': data}, 200

    return {'Status': 'File not allowed'}
