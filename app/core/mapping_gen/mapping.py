import logging
import threading
from pathlib import Path
from time import time
from typing import List, Any, Union
import pandas as pd
import xmlschema
from builtins import str

from pandas import DataFrame

from .MatchVocab import get_vocab_list, matchCompoundToVocab
from .SimilarWordbyModel import getSimilarWordAvg
from .TwoDMatrixOperations import readFile, splitToList
from .MatchPair import isMatchExistscomp
from .ReadWriteFiles import writeCsv
from .MatchVocab import matchWordsModel
from .MatchPair import getValueThreshold
from .StructuralMapping import *
from owlready2 import get_ontology

from ..commons import API_Exception, ErrorCode
from ...app_settings import EXT_MODEL_NAME, UPLOAD_FOLDER, OUTPUT_FOLDER, MAPPING_FOLDER, source_rwc, target_rwc, \
    source_rwd, target_rwd, source_rwo, target_rwo, writepathCompoundc, writepathCompoundd, writepathCompoundo, \
    MAPPING_OUTPUT_FILE, INPUT_FOLDER

out_folder = Path.cwd().joinpath(OUTPUT_FOLDER)
logger = logging.getLogger('mapping_generator')
lock = threading.Lock()


def WordMatchComp(sourcefile: str, targetfile: str, model, vocab_list, unique_file_id: str):
    srcclass, srcdata, srcobj = readFile(UPLOAD_FOLDER, sourcefile)
    targetclass, targetdata, targetobj = readFile(UPLOAD_FOLDER, targetfile)
    logger.info("\n\n\nStep 2: \nfiles read has been done.")

    listSc = splitToList(srcclass)
    listTc = splitToList(targetclass)
    listSd = splitToList(srcdata)
    listTd = splitToList(targetdata)
    listSo = splitToList(srcobj)
    listTo = splitToList(targetobj)
    logger.info("\n\n\nStep 2: \ncompound Lists has been created.")

    # mach to word2vec model vocab
    matchVocab_Sc = matchCompoundToVocab(listSc, vocab_list)
    matchVocab_Tc = matchCompoundToVocab(listTc, vocab_list)
    matchVocab_Sd = matchCompoundToVocab(listSd, vocab_list)
    matchVocab_Td = matchCompoundToVocab(listTd, vocab_list)
    matchVocab_So = matchCompoundToVocab(listSo, vocab_list)
    matchVocab_To = matchCompoundToVocab(listTo, vocab_list)
    logger.info("\n\n\nStep 3: \nMatching and filter with model vocab list has been done.")

    modelMatch_Sc = getSimilarWordAvg(matchVocab_Sc, model, 3)
    modelMatch_Tc = getSimilarWordAvg(matchVocab_Tc, model, 3)
    modelMatch_Sd = getSimilarWordAvg(matchVocab_Sd, model, 3)
    modelMatch_Td = getSimilarWordAvg(matchVocab_Td, model, 3)
    modelMatch_So = getSimilarWordAvg(matchVocab_So, model, 3)
    modelMatch_To = getSimilarWordAvg(matchVocab_To, model, 3)
    logger.info("\n\n\nStep 4: \nGot Similar Words from model")

    mapping_output_location = Path.cwd().joinpath(OUTPUT_FOLDER, unique_file_id)
    if not mapping_output_location.is_dir():
        raise Exception(f'Output folder for {unique_file_id} is missing in STEP 4.')
    writeCsv(modelMatch_Sc, mapping_output_location, source_rwc + unique_file_id + '.csv')
    writeCsv(modelMatch_Tc, mapping_output_location, target_rwc + unique_file_id + '.csv')
    writeCsv(modelMatch_Sd, mapping_output_location, source_rwd + unique_file_id + '.csv')
    writeCsv(modelMatch_Td, mapping_output_location, target_rwd + unique_file_id + '.csv')
    writeCsv(modelMatch_So, mapping_output_location, source_rwo + unique_file_id + '.csv')
    writeCsv(modelMatch_To, mapping_output_location, target_rwo + unique_file_id + '.csv')
    logger.info("\n\n\nStep 5: \nOutput files has been written")

    # matching words/Compound words from source to target using model
    matchPairc, matchPairOriginc = matchWordsModel(modelMatch_Sc, modelMatch_Tc, model)
    matchPaird, matchPairOrigind = matchWordsModel(modelMatch_Sd, modelMatch_Td, model)
    matchPairo, matchPairOrigino = matchWordsModel(modelMatch_So, modelMatch_To, model)
    logger.info("\n\n\nStep 6: \nMatched words from source to taget using model Match.")

    finalMatchPairc, finalMatchPairThreshc = getValueThreshold(matchPairc)
    finalPairOriginc, finalpairOriginThreshc = getValueThreshold(matchPairOriginc)
    finalMatchPaird, finalMatchPairThreshd = getValueThreshold(matchPaird)
    finalPairOrigind, finalpairOriginThreshd = getValueThreshold(matchPairOrigind)
    finalMatchPairo, finalMatchPairThresho = getValueThreshold(matchPairo)
    finalPairOrigino, finalpairOriginThresho = getValueThreshold(matchPairOrigino)
    logger.info("\n\n\nStep 7: \nFiltered threshold on vector value")

    scoresc = []
    if len(scoresc) == 0:
        scoresc: List[List[Union[int, Any]]] = [[finalpairOriginThreshc[0][0], finalpairOriginThreshc[0][2], 0]]
    for inner in finalpairOriginThreshc:
        descisionc, indexc = isMatchExistscomp(inner[0], inner[2], scoresc)
        if descisionc:
            scoresc[indexc][2] = scoresc[indexc][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scoresc.append(tmplist)

    scoresd = []
    if len(scoresd) == 0:
        scoresd: List[List[Union[int, Any]]] = [[finalpairOriginThreshd[0][0], finalpairOriginThreshd[0][2], 0]]
    for inner in finalpairOriginThreshd:
        descisiond, indexd = isMatchExistscomp(inner[0], inner[2], scoresd)
        if descisiond:
            scoresd[indexd][2] = scoresd[indexd][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scoresd.append(tmplist)

    scoreso = []
    if len(scoreso) == 0:
        scoreso: List[List[Union[int, Any]]] = [[finalpairOriginThresho[0][0], finalpairOriginThresho[0][2], 0]]
    for inner in finalpairOriginThresho:
        descisiono, indexo = isMatchExistscomp(inner[0], inner[2], scoreso)
        if descisiono:
            scoreso[indexo][2] = scoreso[indexo][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scoreso.append(tmplist)

    logger.info("\n\n\nStep 8: \nFiltered threshold on vector value")

    writeCsv(scoresc, mapping_output_location, writepathCompoundc + unique_file_id + '.csv')
    writeCsv(scoresd, mapping_output_location, writepathCompoundd + unique_file_id + '.csv')
    writeCsv(scoreso, mapping_output_location, writepathCompoundo + unique_file_id + '.csv')

    ps = Path.cwd().joinpath(UPLOAD_FOLDER, sourcefile)
    schema = xmlschema.XMLSchema(str(ps))
    po = Path.cwd().joinpath(UPLOAD_FOLDER, targetfile)
    onto = get_ontology(str(po)).load()
    logger.info("\n\n\nStep 9: \nReading Schema")

    orgxsdList = srcclass + srcdata + srcobj
    originalXsdList = list(dict.fromkeys(orgxsdList))

    orgowlList = targetclass + targetdata + targetobj
    originalOwlList = list(dict.fromkeys(orgowlList))

    splitSourceList = listSc + listSd + listSo
    splitTargetList = listTc + listTd + listTo
    combineSourceList = [''.join(i) for i in splitSourceList]
    combineTargetList = [''.join(i) for i in splitTargetList]
    jointSourceList = list(dict.fromkeys(combineSourceList))
    jointTargetList = list(dict.fromkeys(combineTargetList))

    combineSourceClass = [''.join(i) for i in listSc]
    combineSourceData = [''.join(i) for i in listSd]
    combineSourceObject = [''.join(i) for i in listSo]

    combineTargetClass = [''.join(i) for i in listTc]
    combineTargetData = [''.join(i) for i in listTd]
    combineTargetObject = [''.join(i) for i in listTo]

    logger.info("\n\n\nStep 10: \n Maintaining Original Terms")

    classMatchList, originalclasslist = cleanInput(scoresc)
    objectMatchList, originalobjectlist = cleanInput(scoreso)
    dataMatchList, originaldatalist = cleanInput(scoresd)

    # getting original Classmapping list from joint and original lists terms
    for i in classMatchList:
        indsrc = getIndex(combineSourceClass, i[0])
        classMatchList[classMatchList.index(i)][0] = srcclass[indsrc]
        indtarget = getIndex(combineTargetClass, i[1])
        classMatchList[classMatchList.index(i)][1] = targetclass[indtarget]

    for i in objectMatchList:
        indsrc = getIndex(combineSourceObject, i[0])
        objectMatchList[objectMatchList.index(i)][0] = srcobj[indsrc]
        indtarget = getIndex(combineTargetObject, i[1])
        objectMatchList[objectMatchList.index(i)][1] = targetobj[indtarget]

    for i in dataMatchList:
        indsrc = getIndex(combineSourceData, i[0])
        dataMatchList[dataMatchList.index(i)][0] = srcdata[indsrc]
        indtarget = getIndex(combineTargetData, i[1])
        dataMatchList[dataMatchList.index(i)][1] = targetdata[indtarget]

    xsdTupleList = getXsdElements(srcclass, schema)

    objectPropertylist = []
    objProp = onto.object_properties()
    for i in objProp:
        range = i.range
        domain = i.domain
        getRange = getSplitStr(range)
        getDomain = getSplitStr(domain)
        property = str(i)
        getProperty = property.split('.')[-1]
        if len(getDomain) > 0 and len(getRange) > 0:
            innerlist = [getDomain, getProperty, getRange]
            objectPropertylist.append(innerlist)
    owlObjectTupleList = sorted(objectPropertylist)

    dataPropertylist = []
    dataProp = onto.object_properties()
    for i in dataProp:
        range = i.range
        domain = i.domain
        getRange = getSplitStr(range)
        getDomain = getSplitStr(domain)
        property = str(i)
        getProperty = property.split('.')[-1]
        if len(getDomain) > 0 and len(getRange) > 0:
            innerlist = [getDomain, getProperty, getRange]
            dataPropertylist.append(innerlist)
    owlDataProperty = sorted(dataPropertylist)

    logger.info("\n\n\nStep 11: \n  Getting Properties if Domain And Range Matches")
    # getting Properties if domian and ranges match
    tmpprop = []
    originalprop = []
    for i in classMatchList:
        sourceMatchList, targetMatchList, = getClassMatchIndexList(xsdTupleList, owlObjectTupleList, i)
        if len(sourceMatchList) > 0 and len(targetMatchList) > 0:
            owlAndXsdRanges, index = getRanges(sourceMatchList, targetMatchList)
            matchRangestoClass = matchPairToClass(owlAndXsdRanges, classMatchList)
            if len(matchRangestoClass) > 0:
                rangeIndex = getIndexForMatchedClasses(matchRangestoClass, index)
                getProperty = getOwlXsdProperties(rangeIndex, xsdTupleList, owlObjectTupleList)
                for i in getProperty:
                    tmpprop.append(i)
                for i in tmpprop:
                    indsrc = getIndex(jointSourceList, i[0])
                    tmpprop[tmpprop.index(i)][0] = originalXsdList[indsrc]
                    indtarget = getIndex(jointTargetList, i[1])
                    tmpprop[tmpprop.index(i)][1] = originalOwlList[indtarget]
    for i in tmpprop:
        i.append(2)

    logger.info("\n\n\nStep 12: \n Getting Domain if Properties And Range Matches")
    # getting domains if properties and ranges match
    tmpdm = []
    for i in objectMatchList:
        xsdPropList, owlPropList = getPropertyMatch(xsdTupleList, owlObjectTupleList, i)
        if len(owlPropList) > 0 and len(xsdPropList) > 0:
            owlXsdRanges, index = getRanges(xsdPropList, owlPropList)
            matchRangestoClass = matchPairToClass(owlXsdRanges, classMatchList)
            if len(matchRangestoClass) > 0:
                rangeIndex = getIndexForMatchedClasses(matchRangestoClass, index)
                getDomain = getOwlXsdDomains(rangeIndex, xsdTupleList, owlObjectTupleList)
                for i in getDomain:
                    tmpdm.append(i)
                for i in tmpdm:
                    indsrc = getIndex(jointSourceList, i[0])
                    tmpdm[tmpdm.index(i)][0] = originalXsdList[indsrc]
                    indtarget = getIndex(jointTargetList, i[1])
                    tmpdm[tmpdm.index(i)][1] = originalOwlList[indtarget]
    for i in tmpdm:
        i.append(2)

    # getting ranges if properties and domain match
    logger.info("\n\n\nStep 13: \n Getting Ranges if Properties And Domain Matches")
    tmprg = []
    for i in objectMatchList:
        xsdPropList, owlPropList = getPropertyMatch(xsdTupleList, owlObjectTupleList, i)
        if len(owlPropList) > 0 and len(xsdPropList) > 0:
            owlXsdDomains, index = getDomains(xsdPropList, owlPropList)
            matchDomianToClass = matchPairToClass(owlXsdDomains, classMatchList)
            if len(matchDomianToClass) > 0:
                domainIndex = getIndexForMatchedClasses(matchDomianToClass, index)
                getRange = getOwlXsdRanges(domainIndex, xsdTupleList, owlObjectTupleList)
                for i in getRange:
                    tmprg.append(i)
                for i in tmprg:
                    indsrc = getIndex(jointSourceList, i[0])
                    tmprg[tmprg.index(i)][0] = originalXsdList[indsrc]
                    indtarget = getIndex(jointTargetList, i[1])
                    tmprg[tmprg.index(i)][1] = originalOwlList[indtarget]
    for i in tmprg:
        i.append(2)

    logger.info("\n\n\nStep 14:Getting Domain and Range if Properties  Matches")
    # getting domian and Range if Property Matches
    tmpdmrg = []
    dmrgoutput = []
    for i in objectMatchList:
        xsdPropList, owlPropList, = getPropertyMatch(xsdTupleList, owlObjectTupleList, i)
        if len(owlPropList) > 0 and len(xsdPropList) > 0:
            domains, index = getDomains(xsdPropList, owlPropList)
            ranges, index = getRanges(xsdPropList, owlPropList)
            for i in domains:
                tmpdmrg.append(i)
            for j in ranges:
                tmpdmrg.append(j)
            removeDuplicate = list(set(map(lambda i: tuple(i), tmpdmrg)))
            dmrgoutput = [list(i) for i in removeDuplicate]
    for i in dmrgoutput:
        i.append(1)

    finallist = tmpprop + tmpdm + tmprg + dmrgoutput + classMatchList + dataMatchList + objectMatchList
    df = pd.DataFrame(finallist, columns=['source_term', 'mapped_term', 'confidence_score'])
    output_file = MAPPING_OUTPUT_FILE + unique_file_id + '.csv'
    df.to_csv(str(out_folder.joinpath(output_file)), index=True)
    logger.info("------------------------- Mapping generation ended. ----------------------------")
    return df


def start_mapping(source_file: Path, target_file: Path, filename_uuid: str) -> DataFrame:
    logger.info('Starting mapping procedure')
    model_location = Path.cwd().joinpath(INPUT_FOLDER, EXT_MODEL_NAME)

    try:
        logger.info('Waiting for mapping lock')
        with lock:
            logger.info('Entered mapping lock')
            logger.info('Loading model and extracting vocabulary list')
            model, vocab_list = get_vocab_list(str(model_location))
            start_time = time()
            logger.info('Starting word matching algorithm')
            df = WordMatchComp(source_file.name, target_file.name, model, vocab_list, filename_uuid)
            logger.info("Mapping procedure completed in: %s seconds" % (time() - start_time))
        return df
    except Exception as e:
        logger.error(f'Something went wrong during mapping procedure\n{e} - {str(e)}')
        raise API_Exception(ErrorCode.GENERIC, 'Mapping process failed')
