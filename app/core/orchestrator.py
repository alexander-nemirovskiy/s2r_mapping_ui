import asyncio
import faulthandler
import logging
from shutil import copyfile, make_archive
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
from typing import Tuple
from uuid import uuid4
from pandas import DataFrame

from .commons import API_Exception, ErrorCode
from .mapping_gen.mapping import start_mapping
from .annotation_pipeline.Step_1_cleaner_selector import cleaner, selector
from .annotation_pipeline.Step_2_type_identification_to_java_annotating \
    import type_identifier_to_java_annotator
from ..app_settings import OUTPUT_FOLDER, INPUT_FOLDER, MAPPING_FOLDER, SELECTOR_OUTPUT_FILE, SOURCE_FILE, TARGET_FILE, \
    MAPPING_OUTPUT_FILE, CLEANED_FILE, SELECTOR_FOLDER, JAR_NAME, JAR_INPUT_PARAM, JAR_OUTPUT_PARAM, WORKER_NUM

logger = logging.getLogger('core-executor')


async def process_xsd_file(input_folder: Path, filename_uuid: str, source_file: Path, target_file: Path):
    logging.info('Creating folder setup')
    input_location = input_folder.joinpath(filename_uuid)
    # input_location.mkdir(parents=True)
    # logging.info('Copying files to required location')
    # copyfile(source_file, input_location.joinpath(SOURCE_FILE))
    # copyfile(target_file, input_location.joinpath(TARGET_FILE))
    logging.info('Executing java command in separate shell')
    command = ' '.join(['java', '-jar', str(input_folder.joinpath(JAR_NAME)),
                        JAR_INPUT_PARAM, str(source_file), JAR_OUTPUT_PARAM,
                        str(input_location)])

    proc = await asyncio.create_subprocess_shell(command,
                                                 stdin=asyncio.subprocess.PIPE,
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.STDOUT)
    logging.info('Shell %s command returned ' % proc.pid)
    stdout, stderr = await proc.communicate()

    logging.info(f'[{command!r} exited with {proc.returncode}]')
    if stdout:
        logging.info(f'[stdout]\n{stdout.decode()}')
    if stderr:
        logging.error(f'[stderr]\n{stderr.decode()}')
        logging.warning('XSD file has not been parsed')
        raise API_Exception(ErrorCode.PARSING, 'XSD file has not been parsed')
    logging.info('Xsd process completed successfully')
    return


async def generate_mapping_pairs(source_file: Path, target_file: Path) -> Tuple[str, DataFrame]:
    faulthandler.enable()

    filename_uuid: str = str(uuid4()).split('-')[0]
    created_filename = MAPPING_OUTPUT_FILE + filename_uuid + '.csv'
    filename_location = Path.cwd().joinpath(OUTPUT_FOLDER, filename_uuid)
    input_location = Path.cwd().joinpath(INPUT_FOLDER, filename_uuid)
    if not filename_location.is_dir():
        filename_location.mkdir(parents=True)
    if not input_location.is_dir():
        input_location.mkdir(parents=True)
    logging.info('Copying files to required OUTPUT location')
    copyfile(source_file, filename_location.joinpath(SOURCE_FILE))
    copyfile(target_file, filename_location.joinpath(TARGET_FILE))
    logging.info('Copying files to required INPUT location')
    copyfile(source_file, input_location.joinpath(SOURCE_FILE))
    copyfile(target_file, input_location.joinpath(TARGET_FILE))
    input_folder = Path.cwd().joinpath(INPUT_FOLDER)
    getXsdStatus = ''
    try:
        await process_xsd_file(input_folder, filename_uuid, source_file, target_file)
        logger.info('Created xsd task')
        loop = asyncio.get_running_loop()
        logger.info('Starting executor for mapping process')
        with ProcessPoolExecutor() as pool:
            logger.info('Using executor pool')
            getXsdStatus = await loop.run_in_executor(pool, start_mapping, source_file, target_file, filename_uuid)
            logger.info('Created file: ' + created_filename)

        logger.info('Exited executor pool block')
    except Exception as e:
        logger.warning('Exception during mapping: ' + str(e))
        raise API_Exception(ErrorCode.GENERIC, 'Mapping failed')

    if not getXsdStatus:
        logger.warning('Mapping process terminated with an error. Please check')
        raise API_Exception(ErrorCode.GENERIC, 'Mapping pairs file not created')
        # TODO testing only
        # getXsdStatus = 'CamelCase'
        # created_filename = 'mapping.csv'
        # filename_location = Path.cwd().joinpath(INPUT_FOLDER)
    faulthandler.disable()
    logger.info('Starting cleaning process...')
    cleaner_df = cleaner(filename_location, created_filename, 'xml2ttl', getXsdStatus)
    logger.info('Cleaning process done!')
    cleaner_df.to_csv(filename_location.joinpath(CLEANED_FILE + filename_uuid + '.csv'))

    sorted_group = cleaner_df.sort_values('confidence_score', ascending=False).groupby('source_term', as_index=False)\
        [['mapped_term', 'confidence_score']].agg(lambda x: list(x))
    return filename_uuid, sorted_group.to_dict()


async def generate_annotations(cleaner_df: DataFrame, automatic: bool, file_id: str):
    output_name: str = SELECTOR_OUTPUT_FILE + file_id + '.csv'
    folder = Path.cwd().joinpath(OUTPUT_FOLDER, file_id)
    if not folder.is_dir():
        raise Exception(f'Output folder for {file_id} is missing in annotation step.')
    out_df = selector(automatic, cleaner_df, folder, output_name)

    input_location = Path.cwd().joinpath(INPUT_FOLDER, file_id)

    final_output_dir = folder.joinpath('annotated_java_files')
    final_output_dir.mkdir(parents=True)

    try:
        type_identifier_to_java_annotator(
            inputs_directory=input_location,
            input_ttl_name=TARGET_FILE,
            outputs_directory=OUTPUT_FOLDER,
            ttl_term_type_csv_name='ttl_term_type_' + file_id + '.csv',
            note_file_name=Path.cwd().joinpath(OUTPUT_FOLDER, file_id, 'notes_' + file_id + '.txt'),
            selected_csv_name=folder.joinpath(output_name),
            input_xml_name=SOURCE_FILE,
            annotated_csv_name=Path.cwd().joinpath(OUTPUT_FOLDER, file_id, 'annotated_output_' + file_id + '.csv'),
            java_files_directory=Path.cwd().joinpath(INPUT_FOLDER, file_id, 'java_classes'),
            final_java_files_directory=final_output_dir,
            user_specified_conversion_type='xml2ttl'
        )
    except Exception as e:
        logger.error(f'Annotation process failed for {file_id} due to exception:\t{e}')
        raise API_Exception(ErrorCode.GENERIC, 'Annotation process failed')


async def get_zip_location(file_id: str) -> Path:
    logger.info(f'Zipping files for {file_id}')
    user_folder = Path.cwd().joinpath(OUTPUT_FOLDER, file_id)
    location = user_folder.joinpath('annotated_java_files')
    make_archive(
        base_dir='annotated_java_files',
        root_dir=user_folder,
        format='zip',
        base_name=location
    )
    logger.info(f'Zipping for {file_id} done!')
    return user_folder.joinpath('annotated_java_files.zip')
