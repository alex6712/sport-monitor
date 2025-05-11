from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session
from repositories import ClientRepository
from services import ClientService


async def get_clients_service(session: Annotated[AsyncSession, Depends(get_session)]):
    client_repo: ClientRepository = ClientRepository(session)

    return ClientService(client_repo)
