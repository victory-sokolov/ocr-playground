import easyocr
from loguru import logger
from .recognizer import Recognizer


class EasyOcr(Recognizer):
    def __init__(self, detail: int = 0) -> None:
        self.reader = easyocr.Reader(["en"], gpu=False)
        self.detail = detail

    def recognize(self, image_path: str):
        logger.info(f"Recognizing image using {self.__class__.__name__}")
        return self.reader.readtext(image_path, detail=self.detail)
