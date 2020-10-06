import os
import shutil

from fastapi import File


def save_file(file: File):
    file_object = file.file
    upload_folder = open(os.path.join("./static", file.filename), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
