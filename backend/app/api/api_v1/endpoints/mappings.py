from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from starlette import status
from starlette.responses import JSONResponse

from ....core.commons import API_Exception, ErrorCode
from ....core.orchestrator import generate_mapping_pairs
from ....utils.file_management import save_upload_file, retrieve_upload_files_by_extension, \
    retrieve_upload_file_by_filename
from ....app_settings import ALLOWED_INPUT_EXTENSIONS, ALLOWED_ONTOLOGY_EXTENSIONS

router = APIRouter()


@router.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    path = Path.cwd().joinpath('uploads', file.filename)
    save_upload_file(file, path)
    return {"filename": file.filename}


@router.get("/files")
def get_filenames(extension: str = ''):
    if extension and (extension in ALLOWED_INPUT_EXTENSIONS or
                      extension in ALLOWED_ONTOLOGY_EXTENSIONS):
        return retrieve_upload_files_by_extension(extension)
    else:
        return retrieve_upload_files_by_extension()


@router.get("/files/{filename}")
async def get_file_by_name(
        filename: str
):
    location = ''
    # TODO stub
    # may also be application/blob
    return FileResponse(location, media_type='application/octet-stream', filename=filename)


@router.get("/mapping")
async def generate_mapping(
        source_filename: str,
        target_filename: str
):
    if not (source_filename and target_filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    else:
        source_file = retrieve_upload_file_by_filename(source_filename)
        target_file = retrieve_upload_file_by_filename(target_filename)
        if not (source_file and target_file):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorCode.GENERIC,
            )
        else:
            # filepath = await start_mapping()
            # return FileResponse(path=filepath)
            res = await generate_mapping_pairs()
            return JSONResponse(content=res)
