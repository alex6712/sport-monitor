from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies.services import get_clients_service
from app.api.dependencies.tokens import validate_access_token
from app.database.tables.entities import User
from app.schemas.v1.responses import ClientsResponse
from app.services import ClientService

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
