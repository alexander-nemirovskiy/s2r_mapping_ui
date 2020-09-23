API_V1_STR = "/api/v1"
PROJECT_NAME = "Shift2Rail"
ALLOWED_HOSTS = [
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://127.0.0.1:4200'
]

# Folder structure
OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'uploads'
INPUT_FOLDER = 'input'
MAPPING_FOLDER = 'mapping'
CLEANED_FILE_FOLDER = 'cleaner'

# external model location
EXT_MODEL_LOCATION = 'uploads/GoogleNews-vectors-negative300.bin'

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