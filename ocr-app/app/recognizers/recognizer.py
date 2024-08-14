from abc import ABC, abstractmethod
from typing import NoReturn


class Recognizer(ABC):
    @abstractmethod
    def recognize(self, image_path: str) -> NoReturn:
        raise NotImplementedError
