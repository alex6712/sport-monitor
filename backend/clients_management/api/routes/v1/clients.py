from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import validate_refresh_token
from api.dependencies.services import get_auth_service
from database.tables.entities import User
from schemas.v1.requests import SignUpRequest
from schemas.v1.responses import StandardResponse, TokenResponse
from services import AuthService

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.get(
    "/test",
    response_model=StandardResponse,
)
def test():
    return {"code": 200, "message": "test"}
