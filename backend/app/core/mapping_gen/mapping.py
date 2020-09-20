from pathlib import Path

from .WordMatchCompound import WordMatchComp
from .MatchVectorCompound import MatchVectorComp
from .CountMatchCompound import CountMatchcomp
from .modelload import loadmodel
from .path import modelpath


def start_mapping(sourcefile, targetfile, number=3):
    # source = sourcefile.name
    # target = targetfile.name
    model, vocablist = loadmodel(modelpath)


    WordMatchComp(sourcefile, targetfile, number, model, vocablist)

    # Matching words from source to target with oneanother
    MatchVectorComp(model)

    # counting pairmatch instances
    finaloutput = CountMatchcomp()
    return finaloutput