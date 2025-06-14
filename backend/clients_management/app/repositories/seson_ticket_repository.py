from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.tables.entities import SeasonTicket
from app.repositories.interface import RepositoryInterface
from app.schemas.v1.requests import SeasonTicketRequest


class SeasonTicketRepository(RepositoryInterface):
    """Репозиторий абонементов.

    Реализация паттерна Репозиторий. Является объектом доступа к данным (DAO).
    Отвечает за взаимодействие с таблицей абонементов и предоставляет базовые CRUD-операции.

    Attributes
    ----------
    session : AsyncSession
        Объект асинхронной сессии SQLAlchemy, используемый для выполнения запросов к базе данных.

    Methods
    -------
    get_season_ticket_by_id(season_ticket_id)
        Возвращает абонемент по его UUID.
    add_season_ticket(season_ticket_data)
        Добавляет новый абонемент в сессию базы данных.
    delete_season_ticket(season_ticket)
        Удаляет абонемент из сессии базы данных.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_season_ticket_by_id(self, season_ticket_id: UUID) -> SeasonTicket:
        """Возвращает абонемент по его уникальному идентификатору (UUID).

        Выполняет SQL-запрос к таблице абонементов и возвращает объект, если он найден.

        Parameters
        ----------
        season_ticket_id : UUID
            Идентификатор абонемента.

        Returns
        -------
        SeasonTicket
            Объект абонемента, если найден, иначе `None`.

        Notes
        -----
        - Использует метод `scalar()` для извлечения одной записи.
        """
        return await self.session.scalar(
            select(SeasonTicket).where(SeasonTicket.id == season_ticket_id)
        )

    async def add_season_ticket(
        self, season_ticket_data: SeasonTicketRequest
    ) -> SeasonTicket:
        """Добавляет новый абонемент в сессию базы данных.

        Создаёт объект модели `SeasonTicket` из данных запроса и добавляет его в текущую сессию.

        Parameters
        ----------
        season_ticket_data : SeasonTicketRequest
            Объект запроса с данными для создания абонемента.

        Returns
        -------
        season_ticket : SeasonTicket
            Добавленная запись абонемента.

        Notes
        -----
        - Метод не выполняет `commit()` — изменения необходимо зафиксировать отдельно.
        - Использует `model_dump()` для преобразования Pydantic-модели в словарь.
        """

        self.session.add(
            season_ticket := SeasonTicket(**season_ticket_data.model_dump())
        )
        await self.session.flush()

        return season_ticket

    async def delete_season_ticket(self, season_ticket: SeasonTicket):
        """Удаляет абонемент из сессии базы данных.

        Помечает объект `season_ticket` для удаления. Удаление вступает в силу после коммита.

        Parameters
        ----------
        season_ticket : SeasonTicket
            Объект абонемента, который требуется удалить.

        Notes
        -----
        - Метод не вызывает `commit()`, это должно быть сделано вызывающим кодом.
        - Удаление происходит асинхронно.
        """
        await self.session.delete(season_ticket)
