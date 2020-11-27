from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from pandas import DataFrame
from starlette import status

from ....core.commons import ErrorCode, OkResponse, MappingPairsResponse, MappingPairsRequest, extract_pair
from ....core.orchestrator import Orchestrator
from ....utils.file_management import save_upload_file, retrieve_upload_files_by_extension, \
    retrieve_upload_file_by_filename, check_allowed_extensions
from ....app_settings import ALLOWED_INPUT_EXTENSIONS, ALLOWED_ONTOLOGY_EXTENSIONS, ANNOTATION_TYPES

router = APIRouter()


@router.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    path = Path.cwd().joinpath('uploads', file.filename)
    save_upload_file(file, path)
    return {"filename": file.filename}


@router.get("/files")
def get_filenames(extensions: List[str] = Query(None)):
    """
    Retrieve all files matching ``extensions`` filter. Returns all the available files if the filter is empty.
    Extensions are prefixed with a period and will be matched against allowed extensions. Empty strings are not allowed.

    Parameters
    ----------
    extensions : `list` [`str`], optional`
        a list containing all the desired extensions with a leading period.

    Returns
    -------
    `list` [`str`]
        All files matching the filter, if any.

    Raises
    ------
    `HTTPException`:
        Raised if wrong file extension has been selected for mapping Bad_Request exception if filter criteria
        have not been met
    """

    if extensions and not (check_allowed_extensions(set(extensions), ALLOWED_INPUT_EXTENSIONS) or
                           check_allowed_extensions(set(extensions), ALLOWED_ONTOLOGY_EXTENSIONS)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Wrong file extension selected for mapping.\n'
                                   'Avaliable extensions for source files include: '
                                   f'{",".join(ALLOWED_INPUT_EXTENSIONS)}\n'
                                   'Avaliable extensions for ontology files include: '
                                   f'{",".join(ALLOWED_ONTOLOGY_EXTENSIONS)}\n')
    return retrieve_upload_files_by_extension(extensions)


@router.get("/files/{filename}")
async def get_annotated_file_zip(
        filename: str
):
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    location = await Orchestrator.get_zip_location(filename)
    # may also be application/blob
    return FileResponse(str(location), media_type='application/zip')


@router.get("/mapping", response_model=MappingPairsResponse)
async def generate_mapping(
        source_filename: str,
        target_filename: str,
        annotation_type: str
):
    """Generates mapping pairs suggestions from an ontology and an input structured file.

    Takes two filenames referring to existing files in the working directory: the first file must be written in a
    structured format while the second one should be an ontology. The application then generates mapping recommendations
    to be used in the annotation process that should follow. In the meantime it converts the source file into
    corresponding Java classes using Java Architecture for XML Binding directives and stores them for future use.
    The process registers a unique code identifier for the current call so that annotated files can be retrieved later on
    using the same information.

    Parameters
    ----------
    source_filename : `str`
        source filename with extension suffix existing in ``upload`` folder.

        Allowed extensions for source file
        - xsd
        - xml

    target_filename : `str`
        target filename with extension suffix existing in ``upload`` folder.

        Allowed extensions for target file
        - owl
        - ttl

    Returns
    -------
    file_id: `str`
        All files matching the filter, if any.

    terms: `dict` [`int`, `str`]
        asd

    options: `dict` [`int`, `list` [`str`]]
        qwe

    scores: `dict` [`int`, `list` [`int`]]

    Raises
    ------
    `HTTPException`:
        Raised if either file has not been selected or could not be found
        resulting in a BadRequest response if filter criteria have not been met

    `API_Exception`:
        Raised if something happens during the mapping process. Check `detail` message to gather
        additional information about what happened.
    """

    if not (source_filename and target_filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    else:
        source_file = retrieve_upload_file_by_filename(source_filename)
        target_file = retrieve_upload_file_by_filename(target_filename)
        if not (source_file and target_file) or annotation_type not in ANNOTATION_TYPES:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorCode.GENERIC,
            )
        else:
            filename_uuid, created_filename, filename_location = await Orchestrator.prepare_host_structure(source_file,
                                                                                                           target_file,
                                                                                                           annotation_type)
            name_id, pairs = await Orchestrator.generate_mapping_pairs(filename_uuid, source_file, target_file)
            # TODO check for breaking code
            pairs = pairs.to_dict()
            return MappingPairsResponse(file_id=name_id, terms=pairs['source_term'], options=pairs['mapped_term'],
                                        scores=pairs['confidence_score'])


@router.get("/mapping/autoselect", response_model=OkResponse)
async def autogenerate_mapping(
        source_filename: str,
        target_filename: str,
        annotation_type: str
):
    """Generates annotated Java files from an ontology and an input structured file using best-match pairing to select
    pairs

    Takes two filenames referring to existing files in the working directory: the first file must be written in a
    structured format while the second one should be an ontology. The application then generates mapping recommendations
    to be used in the annotation process that should follow. In the meantime it converts the source file into
    corresponding Java classes using Java Architecture for XML Binding directives.

    Annotations are generated for these java classes choosing the best-match for the mapping pairing using highest
    confidence score rating defined throughout the generation process.
    Lastly, a unique code identifier for the current call is returned so that annotated files can be retrieved later on
    using the same information.

    Parameters
    ----------
    source_filename : `str`
       source filename with extension suffix existing in ``upload`` folder.

       Allowed extensions for source file
       - xsd
       - xml

    target_filename : `str`
       target filename with extension suffix existing in ``upload`` folder.

       Allowed extensions for target file
       - owl
       - ttl

    annotation_type : `str`
        Allowed extensions for target file
       - java
       - yarrml


    Returns
    -------
    file_id: `str`
       All files matching the filter, if any.

    terms: `dict` [`int`, `str`]
       asd

    options: `dict` [`int`, `list` [`str`]]
       qwe

    scores: `dict` [`int`, `list` [`int`]]

    Raises
    ------
    `HTTPException`:
       Raised if either file has not been selected or could not be found
       resulting in a BadRequest response if filter criteria have not been met

    `API_Exception`:
       Raised if something happens during the mapping process. Check `detail` message to gather
       additional information about what happened.

    """

    if not (source_filename and target_filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.MISSING_PARAMS,
        )
    else:
        source_file = retrieve_upload_file_by_filename(source_filename)
        target_file = retrieve_upload_file_by_filename(target_filename)
        if not (source_file and target_file) or annotation_type not in ANNOTATION_TYPES:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorCode.GENERIC,
            )
        else:
            file_id, created_file, file_location = await Orchestrator.prepare_host_structure(source_file,
                                                                                             target_file,
                                                                                             annotation_type)
            name_id, pairs_df = await Orchestrator.generate_mapping_pairs(file_id, source_file, target_file)
            pairs_df['confidence_score'] = [cs[0] for cs in pairs_df['confidence_score']]
            pairs_df['mapped_term'] = [mt[0] for mt in pairs_df['mapped_term']]
            await Orchestrator.generate_annotations(pairs_df, automatic=True, file_id=name_id)
            return {'task_completed': True, 'message': f'{name_id}'}


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
        await Orchestrator.generate_annotations(cleaned_df, False, confirmedPairs.file_id)
        return {'task_completed': True, 'message': 'mapping completed'}
