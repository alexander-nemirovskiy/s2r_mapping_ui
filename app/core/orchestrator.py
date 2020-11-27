import asyncio
import faulthandler
import logging
from shutil import copyfile, make_archive
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
from typing import Tuple
from uuid import uuid4
from pandas import DataFrame
import configparser

from .annotation_pipeline.yarrrml_generator import YARRRML_mapper
from .commons import API_Exception, ErrorCode
from .mapping_gen.mapping import start_mapping
from .annotation_pipeline.Step_1_cleaner_selector import cleaner, selector
from .annotation_pipeline.Step_2_type_identification_to_java_annotating \
    import type_identifier_to_java_annotator
from ..app_settings import OUTPUT_FOLDER, INPUT_FOLDER, MAPPING_FOLDER, SELECTOR_OUTPUT_FILE, SOURCE_FILE, TARGET_FILE, \
    MAPPING_OUTPUT_FILE, CLEANED_FILE, SELECTOR_FOLDER, JAR_NAME, JAR_INPUT_PARAM, JAR_OUTPUT_PARAM, WORKER_NUM, \
    ALLOWED_INPUT_EXTENSIONS, ALLOWED_ONTOLOGY_EXTENSIONS, ANNOTATION_TYPES, SETTINGS_FILE, MAPPING_SEC, ANNOTATION_KEY, \
    CONVERSION_KEY, ANNOTATED_FOLDER
from ..utils.file_management import check_allowed_extensions

logger = logging.getLogger('core-executor')


class Orchestrator:
    @staticmethod
    async def process_xsd_file(filename_uuid: str):
        logging.info('Creating folder setup')
        input_folder = Path.cwd().joinpath(INPUT_FOLDER)
        input_location = input_folder.joinpath(filename_uuid)
        source_file = input_location.joinpath(SOURCE_FILE)
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

    @staticmethod
    async def generate_mapping_pairs(filename_uuid: str, source_file: Path, target_file: Path) -> Tuple[str, DataFrame]:
        """
        This method makes a separate process to handle the cumbersome mapping process without impacting the current event
        loop. Firstly it prepares the folder structure necessary to receive all the intermediate logs and the outcome files
        the process generates throughout its execution. Then it forwards the given xsd ``source_file`` to a parsing process
        that invokes the jaxb jar in order to generate final java classes to annotate later in the program flow.
        At the end of its execution, the method groups received mappings by their source term and sorts those groups by
        highest confidence score.

        Args:
            filename_uuid: unique identifier for user's folder
            source_file: the xsd file that defines the java classes
            target_file: the ontology file which will handle mapping suggestions

        Returns:
            tuple: a tuple containing:
                - filename_uuid ([str]): hash for the current call
                - sorted_group ([DataFrame]): a ``DataFrame`` containing all mapping pairs grouped by their source term and sorted by
                highest confidence score
        """

        faulthandler.enable()

        df = None
        try:
            loop = asyncio.get_running_loop()
            logger.info('Starting executor for mapping process')
            with ProcessPoolExecutor() as pool:
                logger.info('Using executor pool')
                df = await loop.run_in_executor(pool, start_mapping, source_file, target_file, filename_uuid)

            logger.info('Exited executor pool block')
        except Exception as e:
            logger.warning('Exception during mapping: ' + str(e))
            raise API_Exception(ErrorCode.GENERIC, 'Mapping failed')

        if df is None:
            logger.warning('Mapping process terminated with an error. Please check')
            raise API_Exception(ErrorCode.GENERIC, 'Mapping pairs file not created')
        faulthandler.disable()
        df['confidence_score'] = df['confidence_score'].apply(lambda x: x * 100)
        sorted_group = df.sort_values('confidence_score', ascending=False).groupby('source_term', as_index=False)\
            [['mapped_term', 'confidence_score']].agg(lambda x: list(x))
        return filename_uuid, sorted_group

    @staticmethod
    async def generate_annotations(cleaner_df: DataFrame, automatic: bool, file_id: str):
        output_name: str = SELECTOR_OUTPUT_FILE + file_id + '.csv'
        folder = Path.cwd().joinpath(OUTPUT_FOLDER, file_id)
        if not folder.is_dir():
            raise Exception(f'Output folder for {file_id} is missing in annotation step.')
        config = configparser.ConfigParser()
        config.read(folder.joinpath(SETTINGS_FILE))
        settings = config[MAPPING_SEC]
        input_location = Path.cwd().joinpath(INPUT_FOLDER, file_id)
        selector_df: DataFrame = selector(automatic, cleaner_df, folder, output_name)
        try:
            if settings[ANNOTATION_KEY] == 'java':
                final_output_dir = folder.joinpath(ANNOTATED_FOLDER)
                final_output_dir.mkdir(parents=True)
                await Orchestrator.process_xsd_file(file_id)
                logger.info('Created xsd task')
                type_identifier_to_java_annotator(
                    inputs_directory=input_location,
                    input_ttl_name=TARGET_FILE,
                    outputs_directory=OUTPUT_FOLDER,
                    ttl_term_type_csv_path=Path.cwd().joinpath(OUTPUT_FOLDER, file_id, 'ttl_term_type_' + file_id + '.csv'),
                    note_file_path=Path.cwd().joinpath(OUTPUT_FOLDER, file_id, 'notes_' + file_id + '.txt'),
                    selected_csv_name=folder.joinpath(output_name),
                    input_xml_name=SOURCE_FILE,
                    annotated_csv_name=Path.cwd().joinpath(OUTPUT_FOLDER, file_id, 'annotated_output_' + file_id + '.csv'),
                    java_files_directory=Path.cwd().joinpath(INPUT_FOLDER, file_id, 'java_classes'),
                    final_java_files_directory=final_output_dir,
                    user_specified_conversion_type=settings[CONVERSION_KEY]
                )
            else:
                YARRRML_mapper(input_location, SOURCE_FILE, selector_df, settings[CONVERSION_KEY], folder)
        except Exception as e:
            logger.error(f'Annotation process failed for {file_id} due to exception:\t{e}')
            raise API_Exception(ErrorCode.GENERIC, 'Annotation process failed')

    @staticmethod
    async def prepare_host_structure(source_file, target_file, annotation_type: str) -> Tuple[str, str, Path]:
        filename_uuid: str = str(uuid4()).split('-')[0]
        created_filename = MAPPING_OUTPUT_FILE + filename_uuid + '.csv'
        output_location = Path.cwd().joinpath(OUTPUT_FOLDER, filename_uuid)
        input_location = Path.cwd().joinpath(INPUT_FOLDER, filename_uuid)

        if not output_location.is_dir():
            output_location.mkdir(parents=True)
        if not input_location.is_dir():
            input_location.mkdir(parents=True)

        if not (check_allowed_extensions({source_file.suffix}, ALLOWED_INPUT_EXTENSIONS) and
                check_allowed_extensions({target_file.suffix}, ALLOWED_ONTOLOGY_EXTENSIONS)):
            raise API_Exception(ErrorCode.GENERIC, 'Wrong file extension selected for mapping.\n'
                                                   'Available extensions for source files include: '
                                                   f'{",".join(ALLOWED_INPUT_EXTENSIONS)}\n'
                                                   'Available extensions for ontology files include: '
                                                   f'{",".join(ALLOWED_ONTOLOGY_EXTENSIONS)}\n')

        logging.info('Copying files to required OUTPUT location')
        # copyfile(source_file, output_location.joinpath(SOURCE_FILE + source_file.suffix))
        copyfile(source_file, output_location.joinpath(SOURCE_FILE))
        copyfile(target_file, output_location.joinpath(TARGET_FILE))
        logging.info('Copying files to required INPUT location')
        copyfile(source_file, input_location.joinpath(SOURCE_FILE))
        copyfile(target_file, input_location.joinpath(TARGET_FILE))

        config = configparser.ConfigParser()
        config[MAPPING_SEC] = {
            ANNOTATION_KEY: annotation_type,
            CONVERSION_KEY: 'xml2ttl'
        }
        with open(str(output_location.joinpath(SETTINGS_FILE)), 'w') as configfile:
            config.write(configfile)
        return filename_uuid, created_filename, output_location

    @staticmethod
    async def get_zip_location(file_id: str) -> Path:
        logger.info(f'Zipping files for {file_id}')
        user_folder = Path.cwd().joinpath(OUTPUT_FOLDER, file_id)
        location = user_folder.joinpath(ANNOTATED_FOLDER)
        make_archive(
            base_dir=ANNOTATED_FOLDER,
            root_dir=user_folder,
            format='zip',
            base_name=location
        )
        logger.info(f'Zipping for {file_id} done!')
        return user_folder.joinpath(ANNOTATED_FOLDER, '.zip')




