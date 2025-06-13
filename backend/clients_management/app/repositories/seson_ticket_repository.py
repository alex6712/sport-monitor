from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.tables.entities import SeasonTicket
from app.repositories.interface import RepositoryInterface
from app.schemas.v1.requests import SeasonTicketRequest


class SeasonTicketRepository(RepositoryInterface):
    """Репозиторий абонементов.

    Реализация паттерна Репозиторий. Является объектом доступа к данным (DAO).
    Реализует основные CRUD операции с абонементами.

    Attributes
    ----------
    session : AsyncSession
        Объект асинхронной сессии запроса.

    Methods
    -------
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_season_ticket_by_id(self, season_ticket_id: UUID) -> SeasonTicket:
        return await self.session.scalar(select(SeasonTicket).where(SeasonTicket.id == season_ticket_id))

    async def add_season_ticket(self, season_ticket_data: SeasonTicketRequest):
        self.session.add(SeasonTicket(**season_ticket_data.model_dump()))
