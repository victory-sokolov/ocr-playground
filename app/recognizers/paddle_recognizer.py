from paddleocr import PaddleOCR
from .recognizer import Recognizer

class Paddle(Recognizer):

    def __init__(self) -> None:
        self.ocr_model = PaddleOCR(lang='en')

    def recognize(self, image_path: str):
        data = []
        result = self.ocr_model.ocr(image_path, cls=False)
        for line in result:
            data.append(line[1][0])

        return result

