from .recognizer import Recognizer
import easyocr

class EasyOcr(Recognizer):

    def __init__(self) -> None:
        self.reader = easyocr.Reader(['en'], gpu=False)

    def recognize(self, image_path: str):
        return self.reader.readtext(image_path)
