from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File
from starlette.responses import FileResponse

from ....utils.file_management import save_upload_file, retrieve_mapping_files

router = APIRouter()


@router.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    path = Path.cwd().joinpath('uploads', file.filename)
    save_upload_file(file, path)
    return {"filename": file.filename}


@router.get("/files")
async def get_filenames():
    return retrieve_mapping_files()


@router.get("/files/{filename}")
async def get_file_by_name(
        filename: str
):
    location = ''
    # TODO stub
    # may also be application/blob
    return FileResponse(location, media_type='application/octet-stream', filename=filename)
