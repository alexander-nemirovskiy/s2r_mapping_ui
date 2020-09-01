# Load google model and vocab list

from .path import modelpath
from .MatchVocab import get_vocab_list

# Load google model and vocab list
# model_path= dockerread_writepath+modelname
model_path = modelpath
model, vocab_list = get_vocab_list(model_path)
