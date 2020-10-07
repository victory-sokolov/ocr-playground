import os
import shutil

from fastapi import File


def save_file(file: File) -> None:
    file_object = file.file
    upload_folder = open(os.path.join("./static", file.filename), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()


def is_archive_file(file):
    ext = os.path.splitext(file)[1]
    archive_formats = shutil.get_archive_formats()
    supported_format = [x[0] for x in archive_formats]

    if ext[1:] in supported_format:
        return True

    return False
