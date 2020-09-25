from typing import Optional, List

from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


class ErrorCode:
    GENERIC = "GENERIC_ERROR"
    MISSING_PARAMS = "MISSING_REQUIRED_PARAMETERS"


class API_Exception(Exception):
    def __init__(self, error_code: ErrorCode, message: str = ''):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)


class OkResponse(BaseModel):
    task_completed: bool
    message: Optional[str] = ''


class MappingPairsResponse(BaseModel):
    file_id: str
    pairs: dict


class MappingPairsRequest(BaseModel):
    file_id: str
    pairs: List[dict]


async def http_error_handler(request: Request, exc: API_Exception) -> JSONResponse:
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST,
                        content={'detail': {'code': exc.error_code, 'message': exc.message}})
