API_V1_STR = "/api/v1"
PROJECT_NAME = "Shift2Rail"
ALLOWED_HOSTS = [
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://172.18.0.1',
    'https://172.18.0.1'
]
WORKER_NUM = 8

# Folder structure
OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'uploads'
INPUT_FOLDER = 'input'
MAPPING_FOLDER = 'mapping'
CLEANED_FOLDER = 'cleaner'
SELECTOR_FOLDER = 'selector'

# external model location
EXT_MODEL_NAME = 'GoogleNews-vectors-negative300.bin'

ALLOWED_INPUT_EXTENSIONS = ['xml', 'xsd']
ALLOWED_ONTOLOGY_EXTENSIONS = ['ttl', 'owl']


# * Other Variables
raw_csv_unstructured = True  # True if the out put of the W2V is unstructured
automatic_selection = False  # True if the user is willing to choose just the top scored mappings.

# Intermediate files naming conventions
source_rw = 's_SumArray3'
target_rw = 't_SumArray3'

write_pathVecRaw = 'SumVecRaw'
write_pathVecThr = 'SumVecThr'
write_pathVecOrgRaw = 'SumVecOrgRaw'
write_pathVecOrgThr = 'SumVecOrgThr'

MAPPING_OUTPUT_FILE = 'mapping_results_'
SELECTOR_OUTPUT_FILE = 'selector_'
SOURCE_FILE = 'source'
TARGET_FILE = 'target'
JAR_INPUT_PARAM = '-input'
JAR_OUTPUT_PARAM = '-folder'
JAR_NAME = 'jaxb_impl-0.1.3.jar'
