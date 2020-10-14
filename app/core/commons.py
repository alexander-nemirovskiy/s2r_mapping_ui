from typing import Optional, List, Dict, Tuple

from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


class ErrorCode:
    GENERIC = "GENERIC_ERROR"
    MISSING_PARAMS = "MISSING_REQUIRED_PARAMETERS"
    PARSING = "PARSING_ERROR"


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
    terms: Dict[int, str]
    options: Dict[int, List[str]]
    scores: Dict[int, List[int]]


class MappingPairsRequest(BaseModel):
    file_id: str
    pairs: List[Dict[str, Dict[str, int]]]


async def http_error_handler(request: Request, exc: API_Exception) -> JSONResponse:
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST,
                        content={'detail': {'code': exc.error_code, 'message': exc.message}})


def extract_pair(obj: Dict[str, Dict[str, int]]) -> Tuple[str, str, int]:
    k = next(iter(obj.keys()))
    v = obj.get(k)
    v_k = next(iter(v.keys()))
    v_v = v.get(v_k)
    return k, v_k, v_v
