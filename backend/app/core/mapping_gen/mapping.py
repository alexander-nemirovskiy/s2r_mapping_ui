from .WordMatchCompound import WordMatchComp
from .MatchVectorCompound import MatchVectorComp
from .CountMatchCompound import CountMatchcomp


def start_mapping(sourcefile, targetfile):
    # Getting n numner of matching words for source and taget from model
    WordMatchComp()

    # Matching words from source to target with oneanother
    MatchVectorComp()

    # counting pairmatch instances
    CountMatchcomp()
