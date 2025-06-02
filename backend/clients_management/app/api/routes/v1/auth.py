from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.services import get_auth_service
from app.api.dependencies.tokens import validate_refresh_token
from app.database.tables.entities import User
from app.schemas.v1.requests import SignUpRequest
from app.schemas.v1.responses import StandardResponse, TokenResponse
from app.services import AuthService

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
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Метод аутентификации.

    В теле запроса получает данные аутентификации пользователя (имя пользователя, пароль),
    выполняет аутентификацию и возвращает JWT.

    Parameters
    -----------
    form_data : OAuth2PasswordRequestForm
        Данные аутентификации пользователя.
    auth_service : AuthService
        Объект сервисного слоя обслуживания аутентификации.

    Returns
    -------
    response : TokenResponse
        Модель ответа сервера с вложенной парой JWT.
    """
    return await auth_service.sign_in(form_data)


@router.post(
    "/sign_up",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация.",
)
async def sign_up(
    sign_up_data: Annotated[SignUpRequest, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Метод регистрации.

    Получает модель пользователя (с паролем) в качестве ввода и добавляет запись в базу данных.

    Parameters
    ----------
    sign_up_data : SignUpRequest
        Схема объекта пользователя.
    auth_service : AuthService
        Объект сервисного слоя обслуживания аутентификации.

    Returns
    -------
    response : StandardResponse
        Положительный ответ о регистрации пользователя.
    """
    return await auth_service.sign_up(sign_up_data)


@router.get(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление токена доступа.",
)
async def refresh(
    user: Annotated[User, Depends(validate_refresh_token)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    """Метод повторной аутентификации через токен обновления.

    Получает ``refresh_token`` в заголовке, проверяет на совпадение в базе данных
    используя закодированную информацию, перезаписывает токен обновления в базе данных и
    возвращает новую пару ``access_token`` + ``refresh_token``.

    Parameters
    ----------
    user : User
        Объект пользователя, полученный из зависимости автоматической аутентификации.
    auth_service : AuthService
        Объект сервисного слоя обслуживания аутентификации.

    Returns
    -------
    response : TokenResponse
        Модель ответа сервера с вложенной парой JWT.
    """
    return await auth_service.refresh(user)
