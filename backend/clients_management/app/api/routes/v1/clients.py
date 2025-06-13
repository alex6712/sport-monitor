from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body

from app.api.dependencies.services import get_clients_service
from app.api.dependencies.tokens import validate_access_token
from app.database.tables.entities import User
from app.schemas.v1.requests import AddClientRequest
from app.schemas.v1.responses import (
    ClientsResponse,
    ClientResponse,
    StandardResponse,
)
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
async def all_clients(
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


@router.get(
    "/{uuid}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает информацию о клиенте по его id.",
)
async def client_by_id(
    uuid: UUID,
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    """Получение информации о клиенте по его id.

    Parameters
    ----------
    uuid : UUID
        UUID клиента, по которому запрашивается информация.
    _ : User
        Авторизованный пользователь, полученный через JWT-токен.
    client_service : ClientService
        Объект сервисного слоя для работы с клиентами.

    Returns
    -------
    response : ClientResponse
        Информация о клиенте.

    Notes
    -----
    - Объект пользователя не используется напрямую, но гарантирует проверку авторизации.
    """
    return await client_service.get_client_by_id(uuid)


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавляет запись о новом клиенте.",
)
async def add_client(
    client_data: Annotated[AddClientRequest, Body()],
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    """Добавление нового клиента.

    Этот endpoint обрабатывает POST-запрос и сохраняет нового клиента в системе.
    Доступ к ресурсу возможен только при наличии валидного access токена.

    Parameters
    ----------
    client_data : AddClientRequest
        Данные нового клиента, переданные в теле запроса.
    _ : User
        Авторизованный пользователь. Получает значение через зависимость `validate_access_token`.
    client_service : ClientService
        Сервис для работы с клиентами. Получает значение через зависимость `get_clients_service`.

    Returns
    -------
    StandardResponse
        Стандартный ответ API, содержащий сообщение об успешном создании клиента и/или его идентификатор.

    Raises
    ------
    HTTPException
        Возникает при ошибках валидации данных, отсутствии авторизации или внутренних ошибках сервиса.

    Notes
    -----
    - Требуется авторизация (access токен).
    - Возвращает HTTP статус 201 Created при успешном создании.
    """
    return await client_service.add_client(client_data)
