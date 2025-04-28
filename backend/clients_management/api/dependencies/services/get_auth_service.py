from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session
from repositories import UserRepository
from services import AuthService


async def get_auth_service(session: Annotated[AsyncSession, Depends(get_session)]):
    user_repo: UserRepository = UserRepository(session)

    return AuthService(user_repo)
