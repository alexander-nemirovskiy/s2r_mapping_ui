import asyncio
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from time import sleep
from pandas import DataFrame

from .w2v_2_java_annotation_pipeline.Step_1_cleaner_selector import cleaner, selector
from .w2v_2_java_annotation_pipeline.Step_2_type_identification_to_java_annotating \
    import type_identifier_to_java_annotator
from ..app_settings import OUTPUT_FOLDER

def long_task(t):
    logging.info("2. t: %s", t)
    sleep(3)
    logging.info("4. t: %s", t)
    return t ** 2


async def generate_mapping_pairs(source_file: str, target_file: str) -> DataFrame:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        # TODO substitute with actual library call
        # result = await loop.run_in_executor(pool, start_mapping, source_file, target_file)
        result = await loop.run_in_executor(pool, long_task, 5)
        print(f"Mapping results: [{result}]")
    # return cleaner('output', 'Sumst_MatchCountttl2xml.csv', 'ttl2xml', 'output', 'cleaned_input.csv')
    out_dir = Path.cwd().joinpath(OUTPUT_FOLDER, 'mapping')
    return cleaner(out_dir, 'Sumst_MatchCountttl2xml.csv', 'ttl2xml', 'output', 'cleaned_input.csv')


async def generate_annotations(cleaner_df: DataFrame, automatic: bool):
    #################################

    out_df = selector(automatic, cleaner_df, 'output', 'selector_output.csv')

    # step 2:
    type_identifier_to_java_annotator(
        inputs_directory='input', input_ttl_name='gtfs.ttl',
        outputs_directory='output', ttl_term_type_csv_name='ttl_term_type.csv',
        note_file_name=Path.cwd().joinpath('output', 'notes_location', 'individuals.txt'),
        selected_csv_name=Path.cwd().joinpath('output', 'selector_output.csv'),
        input_xml_name='gtfs.xml', annotated_csv_name=Path.cwd().joinpath('output', 'annotation', 'annotated_output'),
        java_files_directory=Path.cwd().joinpath('input', 'java_classes'),
        final_java_files_directory=Path.cwd().joinpath('output', 'annotated_java_files'),
        user_specified_conversion_type='ttl2xml'
    )
