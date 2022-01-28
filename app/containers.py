from dependency_injector import containers, providers

from processor import Processor
from recognizers import EasyOcr, Paddle, Tesseract


class Recognizers(containers.DeclarativeContainer):
    tesseract = providers.Singleton(Tesseract)
    paddle = providers.Singleton(Paddle)
    easyocr = providers.Singleton(EasyOcr)


class RecognitionContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    recognizers = providers.Container(Recognizers)

    processor = providers.Factory(Processor, recognizer=recognizers.tesseract)
