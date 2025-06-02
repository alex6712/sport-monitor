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
    "/all",
    response_model=ClientsResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает информацию обо всех клиентах.",
)
async def clients(
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    """Получение списка всех клиентов из системы.

    Endpoint предоставляет полный список клиентов, доступный авторизованному пользователю.
    Ответ включает стандартные метаданные и массив объектов клиентов.

    Parameters
    ----------
    _ : User
        Авторизованный пользователь, полученный через JWT-токен.
    client_service : ClientService
        Объект сервисного слоя для работы с клиентами.

    Returns
    -------
    response : ClientsResponse
        Список всех клиентов в БД.

    Notes
    -----
    - Объект пользователя не используется напрямую, но гарантирует проверку авторизации.
    - Возвращает клиентов в алфавитном порядке.
    - Пустой список означает отсутствие клиентов, а не ошибку.
    """
    return await client_service.get_all_clients()
