"""Clients Management API V1

Here are the Version 1 API files.

This file describes the router for API methods of the first version.
"""

from fastapi import APIRouter

from api.v1.endpoints import (
    root_router,
)

api_v1_router = APIRouter(
    prefix="/api/v1",
)
api_v1_router.include_router(root_router)
