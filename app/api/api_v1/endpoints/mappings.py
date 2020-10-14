from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pandas import DataFrame
from starlette import status

from ....core.commons import ErrorCode, OkResponse, MappingPairsResponse, MappingPairsRequest, extract_pair
from ....core.orchestrator import generate_mapping_pairs, generate_annotations, get_zip_location
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
async def get_annotated_file_zip(
        filename: str
):
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    location = await get_zip_location(filename)
    # may also be application/blob
    return FileResponse(str(location), media_type='application/zip')


@router.get("/mapping", response_model=MappingPairsResponse)
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
            name_id, pairs = await generate_mapping_pairs(source_file, target_file)
            return MappingPairsResponse(file_id=name_id, terms=pairs['source_term'], options=pairs['mapped_term'],
                                        scores=pairs['confidence_score'])


@router.get("/mapping/autoselect", response_model=OkResponse)
async def autogenerate_mapping(
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
            name_id, res = await generate_mapping_pairs(source_file, target_file)
            await generate_annotations(res, True, name_id)
            return {'task_completed': True, 'message': 'mapping completed'}


@router.post("/mapping/pairs")
async def confirm_mappings(
        confirmedPairs: MappingPairsRequest
):
    if not (confirmedPairs and confirmedPairs.pairs and confirmedPairs.file_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    else:
        val = list(map(extract_pair, confirmedPairs.pairs))
        cleaned_df = DataFrame(val, columns=['source_term', 'mapped_term', 'confidence_score'])
        await generate_annotations(cleaned_df, False, confirmedPairs.file_id)
        return {'task_completed': True, 'message': 'mapping completed'}
