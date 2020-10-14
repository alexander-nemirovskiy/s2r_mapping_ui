from fastapi import APIRouter

from .endpoints.mappings import router as mapping_router

router = APIRouter()

router.include_router(mapping_router)
