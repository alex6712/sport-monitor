from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories import SeasonTicketRepository
from app.schemas.v1.requests import SeasonTicketRequest
from app.schemas.v1.responses import StandardResponse


class SeasonTicketService:
    """TODO: docstring

    Attributes
    ----------
    season_ticket_repo : SeasonTicketRepository
        Репозиторий абонементов, слой операций с БД.

    Methods
    -------
    """

    def __init__(self, season_ticket_repo: SeasonTicketRepository):
        self.season_ticket_repo: SeasonTicketRepository = season_ticket_repo

    async def add_season_ticket(
        self, season_ticket_data: SeasonTicketRequest
    ) -> StandardResponse:
        try:
            await self.season_ticket_repo.add_season_ticket(season_ticket_data)
            await self.season_ticket_repo.commit()
        except IntegrityError as _:
            await self.season_ticket_repo.rollback()

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Клиент с id={season_ticket_data.client_id} не найден!",
            )

        return StandardResponse(
            code=status.HTTP_201_CREATED,
            message="Абонемент успешно добавлен.",
        )
