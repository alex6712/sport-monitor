from typing import Annotated, AnyStr

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.v1.services import user_service
from core.config import Settings, get_settings
from core.jwt import jwt_decode
from database.tables.entities import User

settings: Settings = get_settings()

engine: AsyncEngine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)
AsyncSessionMaker: async_sessionmaker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Создает уникальный объект асинхронной сессии запроса.

    Используется для добавления сессии базы данных в маршрут запроса, используя систему зависимости FastAPI.

    Returns
    -------
    session : AsyncSession
        Объект асинхронной сессии запроса.
    """
    async with AsyncSessionMaker() as session:
        yield session


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
    return await _get_user_from_token(token, session)


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
    user = await _get_user_from_token(refresh_token := credentials.credentials, session)

    if user.refresh_token != refresh_token:
        raise credentials_exception

    return user


async def _get_user_from_token(token: AnyStr, session: AsyncSession) -> User:
    """Функция для получения записи пользователя из базы данных с помощью данных из JWT.

    Получает JWT в качестве ввода, декодирует его и проверяет, существует ли пользователь в базе данных.
    Возвращает модель записи пользователя из базы данных.

    Parameters
    ----------
    token : AnyStr
        JSON Web Token, токен доступа.
    session : AsyncSession
        Объект сессии запроса.

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

    if (user := await user_service.get_user_by_username(session, username)) is None:
        raise credentials_exception

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()

        raise credentials_exception

    return user
