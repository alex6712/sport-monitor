from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.tables.entities import Client
from app.repositories.interface import RepositoryInterface


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

        Формирует запрос к базе данных на получение списка всех клиентов,
        отсортированного по фамилии пользователя.
        Полученный скаляр переводится в built-in структуру `list`.

        Returns
        -------
        clients : List[Client]
            Список записей пользователей из базы данных.

        Notes
        -----
        - Список клиентов возвращается в алфавитном порядке.
        """
        result = await self.session.scalars(select(Client).order_by(Client.surname))

        return list(result.all())
