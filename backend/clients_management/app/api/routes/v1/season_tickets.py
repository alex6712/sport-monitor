from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
    Body,
    Path,
)

from app.api.dependencies.services import get_season_ticket_service
from app.api.dependencies.tokens import validate_access_token
from app.database.tables.entities import User
from app.schemas.v1.requests import SeasonTicketRequest
from app.schemas.v1.responses import (
    StandardResponse,
)
from app.services import SeasonTicketService

router = APIRouter(
    prefix="/season_tickets",
    tags=["season_tickets"],
)


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавляет запись о новом абонементе.",
)
async def add_season_ticket(
    season_ticket_data: Annotated[SeasonTicketRequest, Body()],
    _: Annotated[User, Depends(validate_access_token)],
    season_ticket_service: Annotated[
        SeasonTicketService, Depends(get_season_ticket_service)
    ],
):
    """Добавляет новый абонемент.

    Создаёт новую запись абонемента на основе переданных данных.
    Требуется авторизация.

    Parameters
    ----------
    season_ticket_data : SeasonTicketRequest
        Данные нового абонемента.
    _ : User
        Авторизованный пользователь (через validate_access_token).
    season_ticket_service : SeasonTicketService
        Сервис для работы с абонементами.

    Returns
    -------
    StandardResponse
        Сообщение об успешном создании абонемента с кодом 201.
    """
    return await season_ticket_service.add_season_ticket(season_ticket_data)


@router.put(
    "/{season_ticket_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновляет запись об абонементе.",
)
async def update_season_ticket(
    season_ticket_id: Annotated[UUID, Path()],
    season_ticket_data: Annotated[SeasonTicketRequest, Body()],
    _: Annotated[User, Depends(validate_access_token)],
    season_ticket_service: Annotated[
        SeasonTicketService, Depends(get_season_ticket_service)
    ],
):
    """Обновляет существующий абонемент по UUID.

    Обновляет данные абонемента с указанным идентификатором.
    Требуется авторизация.

    Parameters
    ----------
    season_ticket_id : UUID
        Уникальный идентификатор абонемента.
    season_ticket_data : SeasonTicketRequest
        Новые данные для абонемента.
    _ : User
        Авторизованный пользователь (через validate_access_token).
    season_ticket_service : SeasonTicketService
        Сервис для работы с абонементами.

    Returns
    -------
    StandardResponse
        Сообщение об успешном обновлении с кодом 200.

    Raises
    ------
    HTTPException
        Возвращается, если абонемент с данным UUID не найден.
    """
    return await season_ticket_service.update_season_ticket(
        season_ticket_id, season_ticket_data
    )


@router.delete(
    "/{season_ticket_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаляет запись об абонементе.",
)
async def delete_season_ticket(
    season_ticket_id: Annotated[UUID, Path()],
    _: Annotated[User, Depends(validate_access_token)],
    season_ticket_service: Annotated[
        SeasonTicketService, Depends(get_season_ticket_service)
    ],
):
    """Удаляет абонемент по UUID.

    Выполняет удаление записи абонемента из базы данных.
    Требуется авторизация.

    Parameters
    ----------
    season_ticket_id : UUID
        Уникальный идентификатор абонемента.
    _ : User
        Авторизованный пользователь (через validate_access_token).
    season_ticket_service : SeasonTicketService
        Сервис для работы с абонементами.

    Returns
    -------
    StandardResponse
        Сообщение об успешном удалении с кодом 200.

    Raises
    ------
    HTTPException
        Возвращается, если абонемент с данным UUID не найден.
    """
    return await season_ticket_service.delete_season_ticket(season_ticket_id)
