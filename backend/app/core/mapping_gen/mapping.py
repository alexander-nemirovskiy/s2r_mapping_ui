import logging
import threading
from pathlib import Path
from time import time
from typing import List, Any, Union
from uuid import uuid4

from .MatchVocab import get_vocab_list, matchCompoundToVocab
from .SimilarWordbyModel import getSimilarWordAvg
from .TwoDMatrixOperations import readFile, splitToList
from .MatchPair import isMatchExistscomp
from .ReadWriteFiles import readTextFile, writeCsv, getStatus
from .TwoDMatrixOperations import makeCompound2dArray
from .MatchVocab import matchWordsModel
from .MatchPair import getValueThreshold
from ..commons import API_Exception, ErrorCode

from ...app_settings import EXT_MODEL_NAME, UPLOAD_FOLDER, OUTPUT_FOLDER, MAPPING_FOLDER, source_rw, target_rw, \
    write_pathVecRaw, write_pathVecThr, write_pathVecOrgRaw, write_pathVecOrgThr, MAPPING_OUTPUT_FILE, INPUT_FOLDER

out_folder = Path.cwd().joinpath(OUTPUT_FOLDER, MAPPING_FOLDER)
logger = logging.getLogger('mapping_generator')
lock = threading.Lock()


def WordMatchComp(sourcefile: str, targetfile: str, model, vocab_list, unique_file_id: str, numberofwords=3) -> str:
    fileS = readFile(UPLOAD_FOLDER, sourcefile)
    fileT = readFile(UPLOAD_FOLDER, targetfile)
    logger.info("Step 1: \n\n\nReading files has been done.")
    getXsdStatus = getStatus(UPLOAD_FOLDER, sourcefile)
    logger.warning(f"xsdStatus retrieved {getXsdStatus}. Going on")

    listS = splitToList(fileS)
    listT = splitToList(fileT)
    logger.info("Step 2: \n\n\ncompound Lists has been created.")

    # mach to word2vec model vocab
    matchVocab_S = matchCompoundToVocab(listS, vocab_list)
    matchVocab_T = matchCompoundToVocab(listT, vocab_list)
    logger.info("Step 3: \n\n\nMatching and filter with model vocab list has been done.")

    modelMatch_S = getSimilarWordAvg(matchVocab_S, model, numberofwords)
    modelMatch_T = getSimilarWordAvg(matchVocab_T, model, numberofwords)
    logger.info("Step 4: \n\n\nGot Similar Words from model")

    mapping_output_location = Path.cwd().joinpath(OUTPUT_FOLDER, MAPPING_FOLDER)
    writeCsv(modelMatch_S, mapping_output_location, source_rw + unique_file_id + '.csv')
    writeCsv(modelMatch_T, mapping_output_location, target_rw + unique_file_id + '.csv')
    logger.info("Step 5: \n\n\nOutput files has been written")
    return getXsdStatus


def MatchVectorComp(model, unique_file_id: str):
    s_data = readTextFile(out_folder, source_rw + unique_file_id + '.csv')
    t_data = readTextFile(out_folder, target_rw + unique_file_id + '.csv')
    logger.info("Step 6: \n\n\nModel written files has been read")

    del t_data[-1]
    del s_data[-1]

    s_array = makeCompound2dArray(s_data)
    t_array = makeCompound2dArray(t_data)
    logger.info("Step 7: \n\n\nMade 2D Array.")

    # matching words/Compound words from source to target using model
    matchPair, matchPairOrigin = matchWordsModel(s_array, t_array, model)
    logger.info("Step 8: \n\n\nMatched words from source to taget using model Match.")

    finalMatchPair, finalMatchPairThresh = getValueThreshold(matchPair)
    finalPairOrigin, finalpairOriginThresh = getValueThreshold(matchPairOrigin)
    logger.info("Step 9: \n\n\nFiltered threshold on vector value")

    writeCsv(finalMatchPair, out_folder, write_pathVecRaw + unique_file_id + '.csv')
    writeCsv(finalMatchPairThresh, out_folder, write_pathVecThr + unique_file_id + '.csv')
    writeCsv(finalPairOrigin, out_folder, write_pathVecOrgRaw + unique_file_id + '.csv')
    writeCsv(finalpairOriginThresh, out_folder, write_pathVecOrgThr + unique_file_id + '.csv')
    logger.info("Step 10: \n\n\nOutput files has been written.")


def CountMatchcomp(unique_file_id: str):
    comFile = readTextFile(out_folder, write_pathVecOrgThr + unique_file_id + '.csv')
    del comFile[-1]
    comp2dArray = makeCompound2dArray(comFile)
    logger.info("Step 11: \n\n\nRead files with threshold")

    scores = []
    if len(scores) == 0:
        scores: List[List[Union[int, Any]]] = [[comp2dArray[0][0], comp2dArray[0][2], 0]]

    for inner in comp2dArray:
        descision, index = isMatchExistscomp(inner[0], inner[2], scores)
        if descision:
            scores[index][2] = scores[index][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scores.append(tmplist)
            tmplist = []

    logger.info("Step 12: \n\n\nCounting similar instances has been done.")
    output_file = MAPPING_OUTPUT_FILE + unique_file_id + '.csv'
    writeCsv(scores, out_folder, output_file)
    logger.info("------------------------- Program has been finished. ----------------------------")


def start_mapping(source_file: Path, target_file: Path, filename_uuid: str) -> str:
    logger.info('Starting mapping procedure')
    model_location = Path.cwd().joinpath(INPUT_FOLDER, EXT_MODEL_NAME)
    getXsdStatus = ''
    try:
        logger.info('Waiting for mapping lock')
        with lock:
            logger.info('Entered mapping lock')
            logger.info('Loading model and extracting vocabulary list')
            model, vocab_list = get_vocab_list(str(model_location))
            start_time = time()
            logger.info('Starting word matching algorithm')
            getXsdStatus = WordMatchComp(source_file.name, target_file.name, model, vocab_list, filename_uuid)
            logger.info('Starting matching algorithm')
            MatchVectorComp(model, filename_uuid)
            logger.info('Count resulting matches')
            CountMatchcomp(filename_uuid)
            logger.info("Mapping procedure completed in: %s seconds" % (time() - start_time))
    except Exception as e:
        logger.error(f'Something went wrong during mapping procedure\n{e} - {str(e)}')
        raise API_Exception(ErrorCode.GENERIC, 'Mapping process failed')
    return getXsdStatus
