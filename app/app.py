import os

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from detect_mrz import get_mrz
from Recognition import Recogniser
from utils.file import save_file

config_name = os.getenv('FLASK_CONFIG', 'default')
app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/upload')
def upload_image(file: UploadFile = File(...)):
    save_file(file)
    mrz = get_mrz(file.filename)

    recogniser = Recogniser('eng', mrz)
    data = recogniser.recognise()

    return {'data': data}, 200
