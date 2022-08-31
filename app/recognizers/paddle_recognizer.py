from paddleocr import PaddleOCR
from loguru import logger
from .recognizer import Recognizer


class Paddle(Recognizer):
    def __init__(
        self,
    ) -> None:
        self.ocr_model = PaddleOCR(
            lang="en",
            use_angle_cls=True,
            show_log=False,
            use_dilation=True
        )

    def recognize(self, image_path: str):
        logger.info(f"Recognizing image using {self.__class__.__name__}")
        result = self.ocr_model.ocr(image_path, cls=False)
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]

        return txts

