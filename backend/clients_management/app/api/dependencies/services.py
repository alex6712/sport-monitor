from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.session import get_session
from app.repositories import (
    ClientRepository,
    UserRepository,
)
from app.services import (
    AuthService,
    ClientService,
)


async def get_auth_service(session: Annotated[AsyncSession, Depends(get_session)]):
    """Создает и возвращает сервис аутентификации с внедренным репозиторием пользователей.

    Parameters
    ----------
    session : AsyncSession
        Асинхронная сессия SQLAlchemy, автоматически внедряемая через Depends.
        Получается из зависимости get_session.

    Returns
    -------
    AuthService
        Экземпляр сервиса аутентификации, инициализированный с репозиторием пользователей.
    """
    user_repo: UserRepository = UserRepository(session)
    return AuthService(user_repo)


async def get_clients_service(session: Annotated[AsyncSession, Depends(get_session)]):
    """Создает и возвращает сервис для работы с клиентами с внедренным репозиторием клиентов.

    Parameters
    ----------
    session : AsyncSession
        Асинхронная сессия SQLAlchemy, автоматически внедряемая через Depends.
        Получается из зависимости get_session.

    Returns
    -------
    ClientService
        Экземпляр сервиса клиентов, инициализированный с репозиторием клиентов.
    """
    client_repo: ClientRepository = ClientRepository(session)
    return ClientService(client_repo)
