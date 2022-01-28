from PIL import Image
from tesserocr import OEM, PyTessBaseAPI

from .recognizer import Recognizer


class Tesseract(Recognizer):
    def __init__(self) -> None:
        pass

    def recognize(self, image_path: str):
        img = Image.open(image_path)
        with PyTessBaseAPI(lang="lav+eng+ocrb", oem=OEM.LSTM_ONLY) as api:
            api.SetImage(img)
            response = api.GetUTF8Text()
            return response
