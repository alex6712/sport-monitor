import re
from typing import AnyStr, Dict

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from core.jwt import create_jwt_pair
from core.security import hash_, verify
from database.tables.entities import User
from repositories import UserRepository
from schemas.v1.requests import SignUpRequest
from schemas.v1.responses import TokenResponse, StandardResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo: UserRepository = user_repo

    async def sign_in(self, form_data: OAuth2PasswordRequestForm):
        user = await self.user_repo.get_user_by_username(form_data.username)

        # проверка на существование пользователя и соответствие пароля
        if not (user and verify(form_data.password, user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenResponse(**await self._get_jwt_pair(user), token_type="bearer")

    async def sign_up(self, sign_up_data: SignUpRequest):
        """Метод регистрации.

        Получает модель пользователя (с паролем) в качестве ввода и добавляет запись в базу данных.

        Parameters
        ----------
        sign_up_data : SignUpRequest
            Схема объекта пользователя.

        Returns
        -------
        response : StandardResponse
            Положительный ответ о регистрации пользователя.
        """
        sign_up_data.password = hash_(sign_up_data.password)

        try:
            await self.user_repo.add_user(sign_up_data)
        except IntegrityError as integrity_error:
            await self.user_repo.session.rollback()

            # Необходимо для тестов, т.к. текст ошибки SQLite отличается от PostgreSQL
            if "sqlite3" in str(integrity_error):
                column, *_ = re.search(r"\.(.*)", str(integrity_error.orig)).groups()
                value: str = sign_up_data.model_dump()[column]

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

        return StandardResponse(
            code=status.HTTP_201_CREATED,
            message="Пользователь создан успешно.",
        )

    async def refresh(self, user: User):
        """Метод повторной аутентификации через токен обновления.

        Получает ``refresh_token`` в заголовке, проверяет на совпадение в базе данных
        используя закодированную информацию, перезаписывает токен обновления в базе данных и
        возвращает новую пару ``access_token`` + ``refresh_token``.

        Parameters
        ----------
        user : User
            Объект пользователя, полученный из зависимости автоматической аутентификации.

        Returns
        -------
        response : TokenResponse
            Модель ответа сервера с вложенной парой JWT.
        """
        return TokenResponse(**await self._get_jwt_pair(user), token_type="bearer")

    async def _get_jwt_pair(self, user: User) -> Dict[AnyStr, AnyStr]:
        """Метод создания новой пары JWT.

        Создает пару ``access_token`` и ``refresh_token``, перезаписывает токен обновления пользователя
        в базе данных и возвращает пару JWT.

        Parameters
        ----------
        user : User
            Объект пользователя.

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
            await self.user_repo.update_refresh_token(user, tokens["refresh_token"])
        except IntegrityError:
            await self.user_repo.session.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect request.",
            )

        return tokens
