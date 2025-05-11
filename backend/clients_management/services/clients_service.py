from repositories import ClientRepository
from schemas.v1.responses import ClientsResponse


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

    async def clients(self) -> ClientsResponse:
        """"""
        return ClientsResponse(clients=await self.client_repo.get_all_clients())
