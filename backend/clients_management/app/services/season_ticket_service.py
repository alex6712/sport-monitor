from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.repositories import SeasonTicketRepository
from app.schemas.v1.requests import SeasonTicketRequest
from app.schemas.v1.responses import StandardResponse


class SeasonTicketService:
    """Сервисный слой для управления абонементами.

    Отвечает за бизнес-логику, связанную с созданием, обновлением и удалением абонементов.
    Делегирует операции с базой данных репозиторию `SeasonTicketRepository`.

    Attributes
    ----------
    season_ticket_repo : SeasonTicketRepository
        Репозиторий абонементов, выполняющий прямое взаимодействие с базой данных.

    Methods
    -------
    add_season_ticket(season_ticket_data)
        Добавляет новый абонемент.
    update_season_ticket(season_ticket_id, season_ticket_data)
        Обновляет существующий абонемент по UUID.
    delete_season_ticket(season_ticket_id)
        Удаляет абонемент по UUID.
    """

    def __init__(self, season_ticket_repo: SeasonTicketRepository):
        self.season_ticket_repo: SeasonTicketRepository = season_ticket_repo

    async def add_season_ticket(
        self, season_ticket_data: SeasonTicketRequest
    ) -> StandardResponse:
        """Добавляет новый абонемент.

        Добавляет абонемент в базу данных и фиксирует изменения.
        В случае нарушения внешнего ключа (например, несуществующий `client_id`)
        возвращает ошибку 404.

        Parameters
        ----------
        season_ticket_data : SeasonTicketRequest
            Объект с данными нового абонемента.

        Returns
        -------
        StandardResponse
            Ответ с кодом 201 и сообщением об успешном добавлении.

        Raises
        ------
        HTTPException
            - 404 Not Found: если связанный клиент не существует.
        """
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
        """Обновляет существующий абонемент по его UUID.

        Находит абонемент по UUID, обновляет поля на основе переданных данных и фиксирует изменения.
        В случае ошибки базы данных или отсутствия записи выбрасывает соответствующее исключение.

        Parameters
        ----------
        season_ticket_id : UUID
            Идентификатор абонемента, который требуется обновить.
        season_ticket_data : SeasonTicketRequest
            Новые данные абонемента.

        Returns
        -------
        StandardResponse
            Ответ с кодом 200 и сообщением об успешном обновлении.

        Raises
        ------
        HTTPException
            - 404 Not Found: если абонемент с данным UUID не найден.
            - 500 Internal Server Error: при неизвестной ошибке коммита.
        """

        season_ticket_record = await self.season_ticket_repo.get_season_ticket_by_id(
            season_ticket_id
        )

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
        """Удаляет абонемент по UUID.

        Находит абонемент по указанному идентификатору и удаляет его из базы данных.
        Если абонемент не найден — возвращает ошибку 404.

        Parameters
        ----------
        season_ticket_id : UUID
            Уникальный идентификатор абонемента.

        Returns
        -------
        StandardResponse
            Ответ с кодом 200 и сообщением об успешном удалении.

        Raises
        ------
        HTTPException
            - 404 Not Found: если абонемент не найден.
        """

        season_ticket = await self.season_ticket_repo.get_season_ticket_by_id(
            season_ticket_id
        )

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
