from abc import ABC, abstractmethod
from PIL import Image

class Recognizer(ABC):

    @abstractmethod
    def recognize(self, image_path: str):
        pass
