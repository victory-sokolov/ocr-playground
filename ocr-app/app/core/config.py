import os
import secrets
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

current_dir = os.getcwd()
dotenv_path = Path(current_dir).parent.parent
load_dotenv(f"{dotenv_path}/.env.local")


class Settings(BaseSettings):
    """Base configuration"""

    APP_NAME: str = "OCR App"
    DEBUG: bool = True
    WRITER_DB_URL: str = os.getenv("WRITER_DB_URL", "")
    READER_DB_URL: str = os.getenv("READER_DB_URL", "")
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    DEBUG_TB_ENABLED: bool = False
    DEBUG_TB_INTERCEPT_REDIRECTS: bool = False
    BCRYPT_LOG_ROUNDS: int = 13
    TOKEN_EXPIRATION_DAYS: int = 30
    TOKEN_EXPIRATION_SECONDS: int = 0
    UPLOAD_FOLDER: str = (
        os.path.abspath(os.curdir)
        + "/"
        + os.getenv(
            "UPLOAD_FOLDER",
            "static",
        )
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

    # class Config:
    #     env_file = env_location
    #     extra = "ignore"
    #     env_ignore_empty = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Settings):
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


def get_config() -> Settings:
    env = os.getenv("ENV", "local")
    config_type = {
        "local": DevelopmentConfig(),
        "prod": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config = get_config()
