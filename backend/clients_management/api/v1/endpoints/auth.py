import re
from typing import Annotated, AnyStr, Dict

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import get_session, validate_refresh_token
from api.v1.services import user_service
from core.jwt import create_jwt_pair
from core.security import hash_, verify
from database.tables.entities import User
from schemas.requests import SignUpRequest
from schemas.responses import StandardResponse, TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["authorization"],
)


@router.post(
    "/sign_in",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Аутентификация.",
)
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод аутентификации.

    В теле запроса получает данные аутентификации пользователя (имя пользователя, пароль),
    выполняет аутентификацию и возвращает JWT.

    Parameters
    -----------
    form_data : OAuth2PasswordRequestForm
        Данные аутентификации пользователя.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : TokenResponse
        Модель ответа сервера с вложенной парой JWT.
    """
    user = await user_service.get_user_by_username(session, form_data.username)

    # проверка на существование пользователя и соответствие пароля
    if not (user and verify(form_data.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {**await _get_jwt_pair(user, session), "token_type": "bearer"}


@router.post(
    "/sign_up",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация.",
)
async def sign_up(
    user: Annotated[SignUpRequest, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод регистрации.

    Получает модель пользователя (с паролем) в качестве ввода и добавляет запись в базу данных.

    Parameters
    ----------
    user : SignUpRequest
        Схема объекта пользователя.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : StandardResponse
        Положительный ответ о регистрации пользователя.
    """
    user.password = hash_(user.password)

    try:
        await user_service.add_user(session, user)
    except IntegrityError as integrity_error:
        await session.rollback()

        # Необходимо для тестов, т.к. текст ошибки SQLite отличается от PostgreSQL
        if "sqlite3" in str(integrity_error):
            column, *_ = re.search(r"\.(.*)", str(integrity_error.orig)).groups()
            value: str = user.model_dump()[column]

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with {column}="{value}" already exists!',
            )
        elif result := re.search(r'"\((.*)\)=\((.*)\)"', str(integrity_error.orig)):
            column, value = result.groups()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with {column}="{value}" already exists!',
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough data in request.",
        )

    return {
        "code": status.HTTP_201_CREATED,
        "message": "User created successfully.",
    }


@router.get(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление токена доступа.",
)
async def refresh(
    user: Annotated[User, Depends(validate_refresh_token)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Метод повторной аутентификации через токен обновления.

    Получает ``refresh_token`` в заголовке, проверяет на совпадение в базе данных
    используя закодированную информацию, перезаписывает токен обновления в базе данных и
    возвращает новую пару ``access_token`` + ``refresh_token``.

    Parameters
    ----------
    user : User
        Объект пользователя, полученный из зависимости автоматической аутентификации.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    response : TokenResponse
        Модель ответа сервера с вложенной парой JWT.
    """
    return {**await _get_jwt_pair(user, session), "token_type": "bearer"}


async def _get_jwt_pair(user: User, session: AsyncSession) -> Dict[AnyStr, AnyStr]:
    """Функция создания новой пары JWT.

    Создает пару ``access_token`` и ``refresh_token``, перезаписывает токен обновления пользователя
    в базе данных и возвращает пару JWT.

    Parameters
    ----------
    user : User
        Объект пользователя.
    session : AsyncSession
        Объект сессии запроса.

    Returns
    -------
    tokens : Dict[AnyStr, AnyStr]
        Пара JWT в форме словаря с двумя ключами: ``access_token`` и ``refresh_token``.

        ``access_token``:
            Токен доступа (``str``).
        ``refresh_token``:
            Токен обновления (``str``).
    """
    tokens = create_jwt_pair({"sub": user.username})

    try:
        await user_service.update_refresh_token(session, user, tokens["refresh_token"])
    except IntegrityError:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect request.",
        )

    return tokens
