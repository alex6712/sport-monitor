from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.tables.entities import Client
from app.repositories.interface import RepositoryInterface
from app.schemas.v1.requests import ClientRequest


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

    async def get_client_by_id(self, client_id: UUID) -> Client:
        """Асинхронно получить объект клиента по его UUID.

        Выполняет запрос к базе данных для поиска клиента с указанным идентификатором.
        Использует SQLAlchemy для асинхронного выполнения запроса.

        Parameters
        ----------
        client_id : UUID
            Уникальный идентификатор клиента, который необходимо найти.

        Returns
        -------
        Client | None
            Объект модели Client, если клиент найден.
            None, если клиент с указанным UUID не существует в базе данных.

        Notes
        -----
        - Метод не вызывает исключений при отсутствии клиента, просто возвращает None
        - Для работы метода требуется активная асинхронная сессия SQLAlchemy (self.session)
        """
        return await self.session.scalar(select(Client).where(Client.id == client_id))

    async def add_client(self, client_data: ClientRequest):
        """Добавляет нового клиента в сессию базы данных.

        Создаёт объект клиента на основе входных данных и добавляет его в текущую сессию SQLAlchemy.
        Коммит выполняется отдельно, после вызова этого метода.

        Parameters
        ----------
        client_data : ClientRequest
            Объект с данными нового клиента. Должен быть совместим с моделью `Client`.
        """
        self.session.add(Client(**client_data.model_dump()))
        await self.commit()
