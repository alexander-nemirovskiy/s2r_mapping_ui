import os
from shutil import copyfileobj
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, List

from fastapi import UploadFile

from app.app_settings import MAPPING_UPLOAD_FOLDER


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None]
) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)
    finally:
        tmp_path.unlink()


def retrieve_mapping_files() -> List[str]:
    path = Path.cwd().joinpath(MAPPING_UPLOAD_FOLDER)
    filenames = []
    for entry in path.iterdir():
        if entry.is_file():
            filenames.append(entry.name)
    return filenames
