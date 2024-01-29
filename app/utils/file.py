import os
import shutil
from os import getcwd, listdir
from os.path import isfile, join

from fastapi import UploadFile
from loguru import logger


def save_file(file: UploadFile) -> None:
    file_name = file.filename
    with open(os.path.join("./app/static", file_name), "wb") as file_object:
        logger.info(f"Storing file {file_name}")
        shutil.copyfileobj(file.file, file_object)


def unarchive_files(f_name: str) -> list[str]:
    logger.info("Archiving files...")
    folder = f"{f_name.split('.')[0]}/"
    # file path where to extract archive images
    file_path = f"app/static/{folder}"
    shutil.unpack_archive(f"{getcwd()}/app/static/{f_name}", file_path)
    files = [folder + f for f in listdir(file_path) if isfile(join(file_path, f))]
    return files


def is_archive_file(file: str) -> bool:
    ext = os.path.splitext(file)[1]
    archive_formats = shutil.get_archive_formats()
    supported_format = [x[0] for x in archive_formats]

    if ext[1:] in supported_format:
        return True

    return False
