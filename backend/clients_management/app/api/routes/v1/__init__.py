from fastapi import APIRouter

from .auth import router as _auth_router
from .clients import router as _clients_router
from .root import router as _root_router
from .season_tickets import router as _season_tickets_router

api_v1_router: APIRouter = APIRouter(prefix="/api/v1")

api_v1_router.include_router(_auth_router)
api_v1_router.include_router(_clients_router)
api_v1_router.include_router(_root_router)
api_v1_router.include_router(_season_tickets_router)
