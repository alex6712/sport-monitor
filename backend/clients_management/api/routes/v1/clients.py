from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dependencies import validate_access_token
from api.dependencies.services import get_clients_service
from database.tables.entities import User
from schemas.v1.responses import ClientsResponse
from services import ClientService

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.get(
    "/",
    response_model=ClientsResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает информацию обо всех клиентах.",
)
async def clients(
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    return await client_service.get_all_clients()
