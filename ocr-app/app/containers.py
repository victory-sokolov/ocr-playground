from dependency_injector import containers
from dependency_injector.providers import Configuration, Container, Factory, Singleton
from processor import Processor
from recognizers import EasyOcr, Tesseract


class Recognizers(containers.DeclarativeContainer):
    tesseract = Singleton(Tesseract)
    # paddle = Singleton(Paddle)
    easyocr = Singleton(EasyOcr)


class RecognitionContainer(containers.DeclarativeContainer):
    config = Configuration()
    recognizer: Container[Recognizers] = Container(Recognizers)

    processor = Factory(Processor, recognizer=recognizer.container.tesseract)
