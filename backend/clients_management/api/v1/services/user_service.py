from typing import AnyStr
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.entities import User
from schemas.requests import SignUpRequest


async def get_user_by_id(session: AsyncSession, id_: UUID) -> User:
    """Возвращает модель пользователя для дальнейшей обработки.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    id_ : UUID
        UUID пользователя.

    Returns
    -------
    user : User
        Модель записи пользователя из базы данных.
    """
    return await session.scalar(select(User).where(User.id == id_))


async def get_user_by_username(session: AsyncSession, username: AnyStr) -> User:
    """Возвращает модель пользователя для дальнейшей обработки.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    username : AnyStr
        Логин пользователя, уникальное имя.

    Returns
    -------
    user : User
        Модель записи пользователя из базы данных.
    """
    return await session.scalar(select(User).where(User.username == username))


async def update_refresh_token(
    session: AsyncSession, user: User, refresh_token: AnyStr
):
    """Перезаписывает токен обновления пользователя.

    Note
    ----
    В этом случае используются функции SQLAlchemy ORM, которые позволяют
    изменить значение атрибута объекта записи пользователя,
    и при закрытии сессии эти изменения будут сохранены в базе данных.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    user : User
        Объект пользователя.
    refresh_token : AnyStr
        Новый токен обновления.
    """
    user.refresh_token = refresh_token
    await session.commit()


async def add_user(session: AsyncSession, user_info: SignUpRequest):
    """Добавляет в базу данных новую запись о сотруднике.

    Parameters
    ----------
    session : AsyncSession
        Объект сессии запроса.
    user_info : SignUpRequest
        Схема объекта пользователя с паролем.
    """
    session.add(User(**user_info.model_dump()))
    await session.commit()
