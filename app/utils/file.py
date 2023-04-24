import os
import shutil

from loguru import logger


def save_file(file) -> None:
    file_name =  file.filename
    with open(os.path.join("./app/static", file_name), "wb") as file_object:
        logger.info(f"Storing file {file_name}")
        shutil.copyfileobj(file.file, file_object)  


def is_archive_file(file: str) -> bool:
    ext = os.path.splitext(file)[1]
    archive_formats = shutil.get_archive_formats()
    supported_format = [x[0] for x in archive_formats]

    if ext[1:] in supported_format:
        return True

    return False
