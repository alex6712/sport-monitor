from app.repositories import ClientRepository
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
        """"""
        return ClientsResponse(clients=await self.client_repo.get_all_clients())
