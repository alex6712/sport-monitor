from fastapi import APIRouter

from .endpoints import (
    auth_router,
    root_router,
)

api_v1_router = APIRouter(
    prefix="/api/v1",
)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(root_router)
