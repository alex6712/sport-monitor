from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
    Body,
    Path,
)

from app.api.dependencies.services import get_clients_service
from app.api.dependencies.tokens import validate_access_token
from app.database.tables.entities import User
from app.schemas.v1.requests import ClientRequest
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
    "/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    summary="Возвращает информацию о клиенте по его id.",
)
async def client_by_id(
    client_id: UUID,
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    """Получение информации о клиенте по его id.

    Parameters
    ----------
    client_id : UUID
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
    return await client_service.get_client_by_id(client_id)


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавляет запись о новом клиенте.",
)
async def add_client(
    client_data: Annotated[ClientRequest, Body()],
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    """Добавление нового клиента.

    Этот endpoint обрабатывает POST-запрос и сохраняет нового клиента в системе.
    Доступ к ресурсу возможен только при наличии валидного access токена.

    Parameters
    ----------
    client_data : ClientRequest
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


@router.put(
    "/{client_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновляет информацию о клиенте.",
)
async def update_client(
    client_id: Annotated[UUID, Path()],
    client_data: Annotated[ClientRequest, Body()],
    _: Annotated[User, Depends(validate_access_token)],
    client_service: Annotated[ClientService, Depends(get_clients_service)],
):
    """Обновляет информацию о существующем клиенте.

    Endpoint обрабатывает PUT-запрос с обновлёнными данными клиента.
    Требует авторизации с использованием access токена. Обновление производится по уникальному идентификатору.

    Parameters
    ----------
    client_id : UUID
         id клиента, чьи данные необходимо обновить.
    client_data : ClientRequest
        Обновлённые данные клиента.
    _ : User
        Авторизованный пользователь. Получает значение через зависимость `validate_access_token`.
    client_service : ClientService
        Сервис для управления клиентами. Получает значение через зависимость `get_clients_service`.

    Returns
    -------
    response : StandardResponse
        Стандартный ответ API с сообщением об успешном обновлении данных клиента.

    Raises
    ------
    HTTPException
        - 404 Not Found: если клиент с указанным идентификатором не найден.
        - 400 Bad Request: если данные некорректны или недостаточны.
        - 409 Conflict: при нарушении уникальных ограничений (например, email уже занят).

    Примечания
    ----------
    - Требуется авторизация.
    - Возвращает HTTP статус 200 OK при успешном обновлении.
    """
    return await client_service.update_client(client_id, client_data)
