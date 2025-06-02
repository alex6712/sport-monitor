from typing import Annotated, AnyStr

from fastapi import Depends, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from app.api.dependencies.services import get_auth_service
from app.core.config import Settings, get_settings
from app.database.tables.entities import User
from app.services import AuthService

settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/{settings.CURRENT_API_URL}/auth/sign_in"
)


async def validate_access_token(
    access_token: Annotated[AnyStr, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Зависимость авторизации.

    Получает JSON Web Token (JWT) в качестве ввода, отправляет на обработку в сервис авторизации.
    Возвращает модель записи пользователя.

    Parameters
    ----------
    access_token : AnyStr
        JSON Web Token, токен доступа.
    auth_service : AuthService
        Сервис авторизации.

    Returns
    -------
    user : User
        Объект пользователя.
    """
    return await auth_service.validate_access_token(access_token)


async def validate_refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Зависимость автоматической авторизации.

    Получает refresh_token пользователя в заголовке запроса, отправляет на обработку в сервис
    авторизации.

    Parameters
    ----------
    credentials : HTTPAuthorizationCredentials
        Данные автоматической авторизации (токен обновления).
    auth_service : AuthService
        Сервис авторизации.

    Returns
    -------
    user : User
        Объект пользователя.
    """
    return await auth_service.validate_refresh_token(credentials.credentials)
