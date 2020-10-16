import uvicorn
from app.main import app

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

        status = start_mapping(sourcefile, targetfile, filename_uuid)
        print(status)
    else:
        uvicorn.run(app, host='127.0.0.1', port=5050, debug=True)
