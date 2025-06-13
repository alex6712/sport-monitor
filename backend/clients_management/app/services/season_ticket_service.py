from uuid import UUID

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

    async def update_season_ticket(
        self,
        season_ticket_id: UUID,
        season_ticket_data: SeasonTicketRequest,
    ) -> StandardResponse:
        season_ticket_record = await self.season_ticket_repo.get_season_ticket_by_id(season_ticket_id)

        if season_ticket_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Абонемент с таким uuid не найден.",
            )

        for key, value in season_ticket_data.model_dump().items():
            setattr(season_ticket_record, key, value)

        try:
            await self.season_ticket_repo.commit()
        except Exception as _:
            await self.season_ticket_repo.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка.",
            )

        return StandardResponse(
            code=status.HTTP_200_OK,
            message="Данные об абонементе успешно обновлены.",
        )

    async def delete_season_ticket(self, season_ticket_id: UUID) -> StandardResponse:
        season_ticket = await self.season_ticket_repo.get_season_ticket_by_id(season_ticket_id)

        if season_ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Абонемент с таким UUID не найден.",
            )

        await self.season_ticket_repo.delete_season_ticket(season_ticket)
        await self.season_ticket_repo.commit()

        return StandardResponse(
            code=status.HTTP_200_OK,
            message="Абонемент успешно удалён.",
        )
