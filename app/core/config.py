import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Base configuration"""

    APP_NAME: str = "OCR App"
    DEBUG: bool = True
    WRITER_DB_URL: str
    READER_DB_URL: str
    SQLALCHEMY_ECHO: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: bytes = os.urandom(24)
    DEBUG_TB_ENABLED: bool = False
    DEBUG_TB_INTERCEPT_REDIRECTS: bool = False
    BCRYPT_LOG_ROUNDS: int = 13
    TOKEN_EXPIRATION_DAYS: int = 30
    TOKEN_EXPIRATION_SECONDS: int = 0
    UPLOAD_FOLDER: str = os.path.abspath(os.curdir) + os.getenv(
        "UPLOAD_FOLDER",
        "static",
    )
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [
        "png",
        "jpg",
        "jpeg",
        "gztar",
        "tar",
        "xztar",
        "zip",
    ]
    OCR_ENGINE: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Settings):
    WRITER_DB_URL: str = ""
    READER_DB_URL: str = ""
    DEBUG_TB_ENABLED: bool = True
    BCRYPT_LOG_ROUNDS: int = 4


class TestConfig(Settings):
    WRITER_DB_URL: str = ""
    READER_DB_URL: str = ""


class ProductionConfig(Settings):
    WRITER_DB_URL: str = ""
    READER_DB_URL: str = ""
    DEBUG: bool = False
    SQLALCHEMY_ECHO: bool = False


def get_config():
    env = os.getenv("ENV", "local")

    config_type = {
        "local": DevelopmentConfig(),
        "prod": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config: Settings = get_config()
