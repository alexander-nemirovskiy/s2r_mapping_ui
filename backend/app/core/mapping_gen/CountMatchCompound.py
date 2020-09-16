from typing import List, Any, Union

from .MatchPair import isMatchExistscomp
from .ReadWriteFiles import readTextFile, writeCsv
from .TwoDMatrixOperations import makeCompound2dArray
from .path import *


def CountMatchcomp():
    read_writepath = standardsOutput
    comFile = readTextFile(read_writepath, readpathCompound)
    del comFile[-1]
    comp2dArray = makeCompound2dArray(comFile)
    print("Step 11: ----------------------->  Read files with threshold")

    scores = []
    if len(scores) == 0:
        scores: List[List[Union[int, Any]]] = [[comp2dArray[0][0], comp2dArray[0][2], 0]]

    for inner in comp2dArray:
        descision, index = isMatchExistscomp(inner[0], inner[2], scores)
        if (descision):
            scores[index][2] = scores[index][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scores.append(tmplist)
            tmplist = []

    print("Step 12: ----------------------->  Counting similar instances has been done.")
    writeCsv(scores, read_writepath, writepathCompound)
    print("------------------------- Program has been finished. ----------------------------")
    return writepathCompound
