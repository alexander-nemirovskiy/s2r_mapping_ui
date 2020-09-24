from pathlib import Path
from typing import List, Dict

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pandas import DataFrame
from starlette import status
from starlette.responses import JSONResponse

from ....core.commons import ErrorCode, OkResponse, MappingPairsResponse
from ....core.orchestrator import generate_mapping_pairs, generate_annotations
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
            # TODO remove hardcoded variables, add paths instead of names
            # source: str = 'it.owl'
            # target = 'Connection.xsd'
            name_id, pairs = await generate_mapping_pairs(source_file, target_file)
            # gb = res.groupby('source_term')['mapped_term'].apply(list).to_dict()
            return MappingPairsResponse(file_id=name_id, pairs=pairs)


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
            # source: str = 'it.owl'
            # target = 'Connection.xsd'
            name_id, res = await generate_mapping_pairs(source_file, target_file)
            await generate_annotations(res, True, name_id)
            return {'task_completed': True, 'message': 'mapping completed'}


def extract_pair(obj: Dict[str, str]):
    k = next(iter(obj.keys()))
    v = obj.get(k)
    return k, v


@router.post("/mapping/pairs", response_model=OkResponse)
async def confirm_mappings(
        confirmedPairs: List[Dict[str, str]],
        file_id: str
):
    if not confirmedPairs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    else:
        val = list(map(extract_pair, confirmedPairs))
        cleaned_df = DataFrame(val, columns=['source_term', 'mapped_term'])
        cleaned_df['confidence_score'] = 100
        await generate_annotations(cleaned_df, False, file_id)
        return {'task_completed': True, 'message': 'mapping completed'}
