from typing import AnyStr
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.entities import User
from schemas.v1.requests import SignUpRequest


class UserRepository:
    """Репозиторий пользователя.

    Реализация паттерна Репозиторий. Является объектом доступа к данным (DAO).
    Реализует основные CRUD операции с пользователями.

    Attributes
    ----------
    session : AsyncSession
        Объект асинхронной сессии запроса.

    Methods
    -------
    get_user_by_id(id_)
        Возвращает модель пользователя по его id.
    get_user_by_username(username)
        Возвращает модель пользователя по его username.
    update_refresh_token(user, refresh_token)
        Перезаписывает токен обновления пользователя.
    add_user(user_info)
        Добавляет в базу данных новую запись о сотруднике.
    """

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_user_by_id(self, id_: UUID):
        """Возвращает модель пользователя по его id.

        Parameters
        ----------
        id_ : UUID
            UUID пользователя.

        Returns
        -------
        user : User
            Модель записи пользователя из базы данных.
        """
        return await self.session.scalar(select(User).where(User.id == id_))

    async def get_user_by_username(self, username: AnyStr) -> User:
        """Возвращает модель пользователя по его username.

        Parameters
        ----------
        username : AnyStr
            Логин пользователя, уникальное имя.

        Returns
        -------
        user : User
            Модель записи пользователя из базы данных.
        """
        return await self.session.scalar(select(User).where(User.username == username))

    async def update_refresh_token(self, user: User, refresh_token: AnyStr):
        """Перезаписывает токен обновления пользователя.

        Note
        ----
        В этом случае используются функции SQLAlchemy ORM, которые позволяют
        изменить значение атрибута объекта записи пользователя,
        и при закрытии сессии эти изменения будут сохранены в базе данных.

        Parameters
        ----------
        user : User
            Объект пользователя.
        refresh_token : AnyStr
            Новый токен обновления.
        """
        user.refresh_token = refresh_token
        await self.session.commit()

    async def add_user(self, user_info: SignUpRequest):
        """Добавляет в базу данных новую запись о сотруднике.

        Parameters
        ----------
        user_info : SignUpRequest
            Схема объекта пользователя с паролем.
        """
        self.session.add(User(**user_info.model_dump()))
        await self.session.commit()
