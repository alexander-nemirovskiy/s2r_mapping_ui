from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .app_settings import ALLOWED_HOSTS, API_V1_STR, PROJECT_NAME
from .api.api_v1.api import router as api_router
from .core.commons import API_Exception, http_error_handler


app = FastAPI(title=PROJECT_NAME,
              version='0.0.1',
              description='First draft of shift to rail mapping software')

# Todo change for production
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(API_Exception, http_error_handler)


app.include_router(api_router, prefix=API_V1_STR)
