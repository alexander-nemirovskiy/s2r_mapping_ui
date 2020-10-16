import uvicorn
from app.main import app


def prepare_host_structure(filename_uuid):
    filename_location = Path.cwd().joinpath('output', filename_uuid)
    input_location = Path.cwd().joinpath('input', filename_uuid)
    if not filename_location.is_dir():
        filename_location.mkdir(parents=True)
    if not input_location.is_dir():
        input_location.mkdir(parents=True)
    return


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        from pathlib import Path
        from uuid import uuid4
        from app.app_settings import UPLOAD_FOLDER
        from app.core.mapping_gen.mapping import start_mapping

        sourcefile = Path.cwd().joinpath(UPLOAD_FOLDER, sys.argv[1])
        targetfile = Path.cwd().joinpath(UPLOAD_FOLDER, sys.argv[2])
        filename_uuid: str = str(uuid4()).split('-')[0]
        prepare_host_structure(filename_uuid)

        status = start_mapping(sourcefile, targetfile, filename_uuid)
        print(status)
    else:
        uvicorn.run(app, host='127.0.0.1', port=5050, debug=True)
