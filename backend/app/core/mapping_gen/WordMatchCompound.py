from .path import *
from .MatchVocab import *
from .ReadWriteFiles import *
from .SimilarWordbyModel import *
from .TwoDMatrixOperations import *


def WordMatchComp(sourcefile, targetfile, numberofwords, model, vocab_list):
    # sourcefile = sys.argv[-2]
    # targetfile = sys.argv[-1]
    fileS = readFile(standardsInput, sourcefile)
    fileT = readFile(standardsInput, targetfile)
    print("Step 1: ------------------------>  Reading files has been done.")

    listS = splitToList(fileS)
    listT = splitToList(fileT)
    print("Step 2: ------------------------>  compound Lists has been created.")

    # mach to word2vec model vocab
    matchVocab_S = matchCompoundToVocab(listS, vocab_list)
    matchVocab_T = matchCompoundToVocab(listT, vocab_list)
    print("Step 3: ----------------------->  Matching and filter with model vocab list has been done.")

    modelMatch_S = getSimilarWordAvg(matchVocab_S, model, numberofwords)
    modelMatch_T = getSimilarWordAvg(matchVocab_T, model, numberofwords)
    print("Step 4: ----------------------->  Got Similar Words from model")

    writeCsv(modelMatch_S, standardsOutput, source_rw)
    writeCsv(modelMatch_T, standardsOutput, target_rw)
    print("Step 5: ----------------------->  Output files has been written")
