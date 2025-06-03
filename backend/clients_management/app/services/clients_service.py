import asyncio

from app.repositories import ClientRepository
from app.schemas.client import CompactClientModel
from app.schemas.v1.responses import ClientsResponse


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
                    email=client.email,
                    phone=client.phone,
                    photo_url=client.photo_url,
                    season_ticket_type=season_ticket_type,
                    is_violator=bool(violations),
                    last_visit=last_visit,
                )
            )

        return ClientsResponse(clients=clients)
