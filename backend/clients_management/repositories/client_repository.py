from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.entities import Client
from repositories.interface import RepositoryInterface


class ClientRepository(RepositoryInterface):
    """Репозиторий клиентов.

    Реализация паттерна Репозиторий. Является объектом доступа к данным (DAO).
    Реализует основные CRUD операции с клиентами.

    Attributes
    ----------
    session : AsyncSession
        Объект асинхронной сессии запроса.

    Methods
    -------
    get_all_clients()
        Возвращает записи всех клиентов в БД.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all_clients(self) -> List[Client]:
        """Возвращает записи всех клиентов в БД.

        Returns
        -------
        clients : List[Client]
            Модель записи пользователя из базы данных.
        """
        result = await self.session.scalars(select(Client).order_by(Client.name))

        return list(result.all())
