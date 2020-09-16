from .path import modelpath
from .MatchVocab import get_vocab_list


# Load google model and vocab list
def loadmodel(modelpath):
    model_path = modelpath
    model, vocab_list = get_vocab_list(model_path)
    return model, vocab_list
