import asyncio
import logging
import shutil
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from time import sleep, time
from typing import Tuple
from uuid import uuid4

from pandas import DataFrame

from .commons import API_Exception, ErrorCode
from .mapping_gen.mapping import start_mapping
from .w2v_2_java_annotation_pipeline.Step_1_cleaner_selector import cleaner, selector
from .w2v_2_java_annotation_pipeline.Step_2_type_identification_to_java_annotating \
    import type_identifier_to_java_annotator
from ..app_settings import OUTPUT_FOLDER, INPUT_FOLDER, MAPPING_FOLDER, SELECTOR_OUTPUT_FILE, SOURCE_FILE, TARGET_FILE, \
    MAPPING_OUTPUT_FILE, CLEANED_FOLDER, SELECTOR_FOLDER, JAR_NAME, JAR_INPUT_PARAM, JAR_OUTPUT_PARAM, UPLOAD_FOLDER


async def generate_mapping_pairs(source_file: Path, target_file: Path) -> Tuple[str, DataFrame]:
    loop = asyncio.get_running_loop()
    created_filename = ''
    filename_uuid: str = str(uuid4()).split('-')[0]
    start_time = time()
    # with ThreadPoolExecutor() as pool:
    # TODO substitute with actual library call
    # filename_uuid: str = await loop.run_in_executor(pool, start_mapping, source_file, target_file, filename_uuid)
    # created_filename = MAPPING_OUTPUT_FILE + filename_uuid + '.csv'
    # logging.info('Created file: ' + created_filename)
    filename_location = Path.cwd().joinpath(OUTPUT_FOLDER, MAPPING_FOLDER)
    logging.info("Mapping process completed in: --- %s seconds ---" % (time() - start_time))
    input_folder = Path.cwd().joinpath(INPUT_FOLDER)

    # copy files to input location for userid
    try:
        input_location = input_folder.joinpath(filename_uuid)
        input_location.mkdir(parents=True)
        shutil.copyfile(source_file, input_location.joinpath(SOURCE_FILE))
        shutil.copyfile(target_file, input_location.joinpath(TARGET_FILE))
        # TODO temp test: change to actual source file
        s_file = Path.cwd().joinpath(UPLOAD_FOLDER, 'example.xsd')
        # command = ' '.join(['java', '-jar', str(input_folder.joinpath(JAR_NAME)),
        #                     JAR_INPUT_PARAM, str(source_file), JAR_OUTPUT_PARAM,
        #                     str(input_location)])
        command = ' '.join(['java', '-jar', str(input_folder.joinpath(JAR_NAME)),
                            JAR_INPUT_PARAM, str(s_file), JAR_OUTPUT_PARAM,
                            str(input_location)])

        proc = await asyncio.create_subprocess_shell(command,
                                                     stdin=asyncio.subprocess.PIPE,
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.STDOUT
                                                     )
        stdout, stderr = await proc.communicate()

        print(f'[{command!r} exited with {proc.returncode}]')
        if stdout:
            logging.info(f'[stdout]\n{stdout.decode()}')
        if stderr:
            logging.error(f'[stderr]\n{stderr.decode()}')
    except Exception as e:
        logging.warning('Exception during user input folder creation: ' + str(e))
        raise API_Exception(ErrorCode.GENERIC, 'Temp file folder creation failed')

    if not created_filename:
        # TODO add exception back and change result to created_filename
        logging.warning('Mapping file not created')
        # raise API_Exception(ErrorCode.GENERIC, 'Mapping pairs file not created')
        created_filename = 'Sumst_MatchCountttl2xml.csv'
    logging.info('Starting cleaning process...')
    cleaner_output_folder = Path.cwd().joinpath(OUTPUT_FOLDER, CLEANED_FOLDER)
    cleaner_df = cleaner(filename_location, created_filename, 'ttl2xml', cleaner_output_folder,
                         filename_uuid + '.csv')
    logging.info('Cleaning process done!')
    return filename_uuid, cleaner_df.groupby('source_term')['mapped_term'].apply(list).to_dict()


async def generate_annotations(cleaner_df: DataFrame, automatic: bool, file_id: str):
    output_name: str = SELECTOR_OUTPUT_FILE + file_id + '.csv'
    selector_output_folder = Path.cwd().joinpath(OUTPUT_FOLDER, SELECTOR_FOLDER)
    out_df = selector(automatic, cleaner_df, selector_output_folder, output_name)

    input_location = Path.cwd().joinpath(INPUT_FOLDER, file_id)

    final_output_dir = Path.cwd().joinpath(OUTPUT_FOLDER, 'annotated_java_files', file_id)
    final_output_dir.mkdir(parents=True)
    # call to maven script

    # input_ttl_name = 'gtfs.ttl'
    type_identifier_to_java_annotator(
        inputs_directory=input_location, input_ttl_name=TARGET_FILE,
        outputs_directory=OUTPUT_FOLDER, ttl_term_type_csv_name='ttl_term_type_' + file_id + '.csv',
        note_file_name=Path.cwd().joinpath(OUTPUT_FOLDER, 'notes_location', 'individuals_' + file_id + '.txt'),
        selected_csv_name=selector_output_folder.joinpath(output_name),
        input_xml_name=SOURCE_FILE, annotated_csv_name=Path.cwd().joinpath(OUTPUT_FOLDER, 'annotation',
                                                                           'annotated_output_' + file_id),
        java_files_directory=Path.cwd().joinpath(INPUT_FOLDER, 'java_classes'),
        final_java_files_directory=final_output_dir,
        user_specified_conversion_type='ttl2xml'
    )


async def get_zip_location(file_id: str) -> Path:
    location = Path.cwd().joinpath(OUTPUT_FOLDER, 'annotated_java_files')
    user_folder = location.joinpath(file_id)
    shutil.make_archive(user_folder, 'zip', location, file_id)
    return location.joinpath(file_id + '.zip')
