API_V1_STR = "/api/v1"
PROJECT_NAME = "Shift2Rail"
ALLOWED_HOSTS = [
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://127.0.0.1:4200'
]
OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'uploads'
CLEANED_FILE_FOLDER = 'cleaner'
ALLOWED_INPUT_EXTENSIONS = ['xml', 'xsd']
ALLOWED_ONTOLOGY_EXTENSIONS = ['ttl', 'owl']


# * Other Variables
raw_csv_unstructured = True  # True if the out put of the W2V is unstructured
automatic_selection = False  # True if the user is willing to choose just the top scored mappings.
