import asyncio
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from time import sleep
from uuid import uuid4

from pandas import DataFrame

from .commons import API_Exception, ErrorCode
from .mapping_gen.mapping import start_mapping
from .w2v_2_java_annotation_pipeline.Step_1_cleaner_selector import cleaner, selector
from .w2v_2_java_annotation_pipeline.Step_2_type_identification_to_java_annotating \
    import type_identifier_to_java_annotator
from ..app_settings import OUTPUT_FOLDER, INPUT_FOLDER, MAPPING_FOLDER, SELECTOR_OUTPUT_FILE


def long_task(t):
    logging.info("First info. t: %s", t)
    sleep(3)
    logging.info("Second info. t: %s", t)
    return t ** 2


async def generate_mapping_pairs(source_file: Path, target_file: Path):
    loop = asyncio.get_running_loop()
    created_filename = ''
    filename_uuid: str = str(uuid4()).split('-')[0]
    with ThreadPoolExecutor() as pool:
        # TODO substitute with actual library call
        #filename_uuid: str = await loop.run_in_executor(pool, start_mapping, source_file, target_file, filename_uuid)
        #created_filename = MAPPING_OUTPUT_FILE + filename_uuid + '.csv'
        result = await loop.run_in_executor(pool, long_task, 5)
        print(f"Mapping results: [{result}]")
    filename_location = Path.cwd().joinpath(OUTPUT_FOLDER, MAPPING_FOLDER)
    if not created_filename:
        # TODO add exception back and change result to created_filename
        # raise API_Exception(ErrorCode.GENERIC, 'Mapping pairs file not created')
        created_filename = 'Sumst_MatchCountttl2xml.csv'
    cleaner_df = cleaner(filename_location, created_filename, 'ttl2xml', OUTPUT_FOLDER, 'cleaned_input_' + filename_uuid + '.csv')
    return filename_uuid, cleaner_df.groupby('source_term')['mapped_term'].apply(list).to_dict()


async def generate_annotations(cleaner_df: DataFrame, automatic: bool, file_id: str):
    output_name: str = SELECTOR_OUTPUT_FILE + file_id + '.csv'
    out_df = selector(automatic, cleaner_df, OUTPUT_FOLDER, output_name)

    type_identifier_to_java_annotator(
        inputs_directory=INPUT_FOLDER, input_ttl_name='gtfs.ttl',
        outputs_directory=OUTPUT_FOLDER, ttl_term_type_csv_name='ttl_term_type_' + file_id + '.csv',
        note_file_name=Path.cwd().joinpath(OUTPUT_FOLDER, 'notes_location', 'individuals_' + file_id + '.txt'),
        selected_csv_name=Path.cwd().joinpath(OUTPUT_FOLDER, output_name),
        input_xml_name='gtfs.xml', annotated_csv_name=Path.cwd().joinpath(OUTPUT_FOLDER, 'annotation',
                                                                          'annotated_output_' + file_id),
        java_files_directory=Path.cwd().joinpath(INPUT_FOLDER, 'java_classes'),
        final_java_files_directory=Path.cwd().joinpath(OUTPUT_FOLDER, 'annotated_java_files', file_id),
        user_specified_conversion_type='ttl2xml'
    )
