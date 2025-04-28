from typing import Annotated, AnyStr

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session
from core.config import Settings, get_settings
from core.jwt import jwt_decode
from database.tables.entities import User
from repositories import UserRepository

settings: Settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/{settings.CURRENT_API_URL}/auth/sign_in"
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


async def validate_access_token(
    token: Annotated[AnyStr, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """Зависимость авторизации.

    Получает JSON Web Token (JWT) в качестве ввода, декодирует его и проверяет, существует ли пользователь в базе данных.
    Возвращает модель записи пользователя.

    Parameters
    ----------
    token : AnyStr
        JSON Web Token, токен доступа.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    user : User
        Объект пользователя.
    """
    return await _get_user_from_token(token, UserRepository(session))


async def validate_refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """Зависимость автоматической авторизации.

    Получает refresh_token пользователя в заголовке запроса, декодирует его,
    проверяет на совпадение в базе данных.

    Parameters
    ----------
    credentials : HTTPAuthorizationCredentials
        Данные автоматической авторизации (токен обновления).
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    user : User
        Объект пользователя.
    """
    user = await _get_user_from_token(
        refresh_token := credentials.credentials, UserRepository(session)
    )

    if user.refresh_token != refresh_token:
        raise credentials_exception

    return user


async def _get_user_from_token(token: AnyStr, user_repo: UserRepository) -> User:
    """Функция для получения записи пользователя из базы данных с помощью данных из JWT.

    Получает JWT в качестве ввода, декодирует его и проверяет, существует ли пользователь в базе данных.
    Возвращает модель записи пользователя из базы данных.

    Parameters
    ----------
    token : AnyStr
        JSON Web Token, токен доступа.
    user_repo : UserRepository
        Объект доступа к данным пользователя.

    Returns
    -------
    user : User
        Модель записи пользователя из базы данных.
    """
    try:
        if (username := jwt_decode(token).get("sub")) is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Signature has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception

    if (user := await user_repo.get_user_by_username(username)) is None:
        raise credentials_exception

    try:
        await user_repo.session.commit()
    except IntegrityError:
        await user_repo.session.rollback()

        raise credentials_exception

    return user
