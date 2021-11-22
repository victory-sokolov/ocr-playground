from dependency_injector import containers, providers
from processor import Processor
from recognizers import Tesseract, Paddle, EasyOcr

class Recognizers(containers.DeclarativeContainer):
    tesseract = providers.Singleton(Tesseract)
    padle = providers.Singleton(Paddle)
    easyocr = providers.Singleton(EasyOcr)

class RecognitionContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    recognizers = providers.Container(Recognizers)

    processor = providers.Factory(
        Processor,
        recognizer=recognizers.tesseract
    )
