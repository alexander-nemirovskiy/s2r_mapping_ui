API_V1_STR = "/api/v1"
PROJECT_NAME = "Shift2Rail"
ALLOWED_HOSTS = [
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://172.17.0.1',
    'https://172.17.0.1'
]
WORKER_NUM = 8

# Folder structure
OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'uploads'
INPUT_FOLDER = 'input'
MAPPING_FOLDER = 'mapping'
SELECTOR_FOLDER = 'selector'

# external model location
# EXT_MODEL_NAME = 'GoogleNews-vectors-negative300.bin'
EXT_MODEL_NAME = 'model.bin'

ALLOWED_INPUT_EXTENSIONS = {'.xml', '.xsd'}
ALLOWED_ONTOLOGY_EXTENSIONS = {'.ttl', '.owl'}


# * Other Variables
raw_csv_unstructured = True  # True if the out put of the W2V is unstructured
automatic_selection = False  # True if the user is willing to choose just the top scored mappings.

# Intermediate files naming conventions
source_rwc = 's_SumArray3c'
source_rwd = 's_SumArray3d'
source_rwo = 's_SumArray3o'
target_rwc = 't_SumArray3c'
target_rwd = 't_SumArray3d'
target_rwo = 't_SumArray3o'

writepathCompoundc= 'Sumst_MatchCountc'
writepathCompoundd= 'Sumst_MatchCountd'
writepathCompoundo= 'Sumst_MatchCounto'

MAPPING_OUTPUT_FILE = 'mapping_results_'
CLEANED_FILE = 'cleaner_'
SELECTOR_OUTPUT_FILE = 'selector_'
SOURCE_FILE = 'source'
TARGET_FILE = 'target'
JAR_INPUT_PARAM = '-input'
JAR_OUTPUT_PARAM = '-folder'
JAR_NAME = 'jaxb_impl-0.1.3.jar'
