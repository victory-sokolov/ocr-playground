import os
from typing import List

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    UPLOAD_FOLDER = os.path.abspath(os.curdir) + os.getenv("UPLOAD_FOLDER", "static")
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [
        "png",
        "jpg",
        "jpeg",
        "gztar",
        "tar",
        "xztar",
        "zip",
    ]
    OCR_ENGINE = os.getenv("OCR_ENGINE")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    WRITER_DB_URL = os.getenv("WRITER_DB_URL")
    READER_DB_URL = os.getenv("READER_DB_URL")
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4


class TestConfig(BaseConfig):
    """Testing configuration"""

    TESTING = False
    DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class ProductionConfig(BaseConfig):
    pass


def get_config() -> BaseConfig:
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestConfig(),
        "local": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config = get_config()
