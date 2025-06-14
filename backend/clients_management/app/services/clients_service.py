import asyncio
import re
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.database.tables.entities import Client
from app.repositories import ClientRepository
from app.schemas.client import CompactClientModel, ClientModel
from app.schemas.group import CompactGroupModel
from app.schemas.season_ticket import SeasonTicketModel
from app.schemas.v1.requests import ClientRequest
from app.schemas.v1.responses import (
    ClientResponse,
    ClientsResponse,
    CreatedResponse,
    StandardResponse,
)


class ClientService:
    """TODO: docstring

    Attributes
    ----------
    client_repo : ClientRepository
        Репозиторий клиентов, слой операций с БД.

    Methods
    -------
    """

    def __init__(self, client_repo: ClientRepository):
        self.client_repo: ClientRepository = client_repo

    async def get_all_clients(self) -> ClientsResponse:
        """Получение краткой информации обо всех клиентах.

        Метод получает все записи клиентов из репозитория и преобразует их
        в компактное представление, подходящее для отображения списка.
        Для каждого клиента дополнительно загружает:
        - Тип текущего абонемента (если есть)
        - Наличие нарушений
        - Дату последнего посещения (если есть)

        Возвращает
        --------
        response : ClientsResponse
            Объект ответа, содержащий список экземпляров CompactClientModel.

        Примечания
        --------
        - Метод выполняет дополнительные асинхронные запросы для связанных данных,
          что может повлиять на производительность при большом количестве клиентов.
        - Учитывается только текущий абонемент и последнее посещение, если их несколько.
        - Флаг нарушений имеет значение True, если у клиента есть хотя бы одно нарушение.
        """
        records = await self.client_repo.get_all_clients()

        clients = []
        for client in records:
            season_tickets, visits, violations = await asyncio.gather(
                client.awaitable_attrs.season_tickets,
                client.awaitable_attrs.visits,
                client.awaitable_attrs.violations,
            )

            season_ticket_type = season_tickets[0].type if season_tickets else None
            last_visit = visits[0].visit_start.date() if visits else None

            clients.append(
                CompactClientModel(
                    id=client.id,
                    name=client.name,
                    surname=client.surname,
                    patronymic=client.patronymic,
                    sex=client.sex,
                    email=client.email,
                    phone=client.phone,
                    photo_url=client.photo_url,
                    season_ticket_type=season_ticket_type,
                    is_violator=bool(violations),
                    last_visit=last_visit,
                )
            )

        return ClientsResponse(clients=clients)

    async def get_client_by_id(self, client_id: UUID) -> ClientResponse:
        """Получить информацию о клиенте по его UUID.

        Асинхронный метод, который возвращает полную информацию о клиенте,
        включая данные о группах и абонементах, в формате ClientResponse.

        Parameters
        ----------
        client_id : UUID
            Уникальный идентификатор клиента, по которому осуществляется поиск.

        Returns
        -------
        ClientResponse
            Объект ответа, содержащий модель клиента со всей сопутствующей информацией.

        Raises
        -------
        HTTPException
            - 404 NOT_FOUND: если клиент с указанным UUID не найден в репозитории.
        """
        client_record = await self.client_repo.get_client_by_id(client_id)

        if client_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент с таким uuid не найден.",
            )

        group_records, season_ticket_records = await asyncio.gather(
            client_record.awaitable_attrs.groups,
            client_record.awaitable_attrs.season_tickets,
        )

        groups: List[CompactGroupModel] = list()
        for group in group_records:
            groups.append(
                CompactGroupModel(
                    id=group.id,
                    type=group.type,
                    quantity=len(await group.awaitable_attrs.clients),
                )
            )

        season_tickets: List[SeasonTicketModel] = list()
        for season_ticket in season_ticket_records:
            season_tickets.append(
                SeasonTicketModel(
                    id=season_ticket.id,
                    type=season_ticket.type,
                    expires_at=str(season_ticket.expires_at),
                )
            )

        client = ClientModel(
            id=client_record.id,
            name=client_record.name,
            surname=client_record.surname,
            patronymic=client_record.patronymic,
            sex=client_record.sex,
            email=client_record.email,
            phone=client_record.phone,
            photo_url=client_record.photo_url,
            groups=groups,
            season_tickets=season_tickets,
        )

        return ClientResponse(client=client)

    async def add_client(self, client_data: ClientRequest) -> CreatedResponse:
        """Добавляет нового клиента в базу данных.

        Пытается создать новую запись клиента на основе переданных данных.
        В случае нарушения ограничений целостности (например, дублирующее значение уникального поля)
        возвращает соответствующую ошибку.

        Parameters
        ----------
        client_data : ClientRequest
            Данные для создания нового клиента. Включают поля, необходимые для добавления клиента
            (например, имя, email и т.д.).

        Returns
        -------
        CreatedResponse
            Объект ответа с кодом 201 и сообщением об успешном создании клиента.

        Raises
        ------
        HTTPException
            - 409 Conflict: если клиент с такими уникальными данными уже существует.
            - 400 Bad Request: если в запросе недостаточно данных для создания клиента.

        Notes
        -----
        - Использует `client_repo.add_client()` для сохранения клиента.
        - В случае ошибки вызывает `client_repo.rollback()`.
        - Производит парсинг сообщения об ошибке базы данных для извлечения конфликтующего столбца и значения.
        """
        try:
            client: Client = await self.client_repo.add_client(client_data)
            await self.client_repo.commit()
        except IntegrityError as integrity_error:
            await self.client_repo.rollback()

            if result := re.search(r'"\((.*)\)=\((.*)\)"', str(integrity_error.orig)):
                column, value = result.groups()

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'User with {column}="{value}" already exists!',
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough data in request.",
            )

        return CreatedResponse(
            message="Клиент создан успешно.",
            id=client.id,
        )

    async def update_client(
        self, client_id: UUID, client_data: ClientRequest
    ) -> StandardResponse:
        """Обновляет данные существующего клиента по его UUID.

        Получает текущую запись клиента из базы данных и обновляет её на основе переданных данных.
        Если клиент с указанным UUID не найден, возбуждает исключение.

        Parameters
        ----------
        client_id : UUID
            Уникальный идентификатор клиента, чьи данные необходимо обновить.
        client_data : ClientRequest
            Объект, содержащий новые значения полей клиента.

        Returns
        -------
        StandardResponse
            Ответ с кодом 200 и сообщением об успешном обновлении.

        Raises
        ------
        HTTPException
            - 404 Not Found: если клиент с указанным UUID не найден.
            - 409 Conflict: если нарушено условие целостности.
            - 500 Internal Server Error: при неопределённом поведении.

        Notes
        -----
        - Использует `get_client_by_id()` для получения текущих данных клиента.
        - Все поля из `client_data` переносятся в объект клиента через `setattr`.
        - Транзакция сохраняется вызовом `commit()` в `client_repo`.
        """
        client_record = await self.client_repo.get_client_by_id(client_id)

        if client_record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент с таким uuid не найден.",
            )

        for key, value in client_data.model_dump().items():
            setattr(client_record, key, value)

        try:
            await self.client_repo.commit()
        except IntegrityError as integrity_error:
            await self.client_repo.rollback()

            if result := re.search(r'"\((.*)\)=\((.*)\)"', str(integrity_error.orig)):
                column, value = result.groups()

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'Client with {column}="{value}" already exists!',
                )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Неизвестная ошибка.",
            )

        return StandardResponse(message="Данные о клиенте успешно обновлены.")

    async def delete_client(self, client_id: UUID) -> StandardResponse:
        """Удаляет клиента из базы данных по UUID.

        Проверяет наличие клиента по указанному UUID. Если клиент найден — удаляет его
        и коммитит изменения в базу данных. В противном случае выбрасывает исключение.

        Parameters
        ----------
        client_id : UUID
            Уникальный идентификатор клиента, которого нужно удалить.

        Returns
        -------
        StandardResponse
            Ответ с кодом 200 и сообщением об успешном удалении клиента.

        Raises
        ------
        HTTPException
            - 404 Not Found: если клиент не найден.

        Notes
        -----
        - Использует метод `get_client_by_id()` из репозитория.
        - После удаления вызывает `commit()` для сохранения изменений.
        """

        client = await self.client_repo.get_client_by_id(client_id)

        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент с таким UUID не найден.",
            )

        await self.client_repo.delete_client(client)
        await self.client_repo.commit()

        return StandardResponse(message="Клиент успешно удалён.")
