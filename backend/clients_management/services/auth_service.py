import re
from typing import AnyStr, Dict

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.exc import IntegrityError

from core.config import Settings, get_settings
from core.jwt import create_jwt_pair, jwt_decode
from core.security import hash_, verify
from database.tables.entities import User
from repositories import UserRepository
from schemas.v1.requests import SignUpRequest
from schemas.v1.responses import TokenResponse, StandardResponse

settings: Settings = get_settings()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


class AuthService:
    """Сервис аутентификации и авторизации.

    Является сервисным слоем приложения, реализующим бизнес-логику
    работы с пользователями приложения.

    Осуществляет операции регистрации, аутентификации, обновления и генерации токенов,
    операции авторизации (валидации токена доступа и токена обновления).

    Attributes
    ----------
    user_repo : UserRepository
        Репозиторий пользователя, слой операций с БД.

    Methods
    -------
    sign_in(form_data)
        Реализует бизнес-логику аутентификации пользователя.
    sign_up(sign_up_data)
        Реализует бизнес-логику регистрации пользователя.
    refresh(user)
        Реализует бизнес-логику повторной аутентификации пользователя.
    validate_access_token(access_token)
        Реализует бизнес-логику авторизации по токену доступа.
    validate_refresh_token(refresh_token)
        Реализует бизнес-логику авторизации по токену обновления.
    _get_jwt_pair(user)
        Генерирует новую пару JWT.
    _get_user_from_token(token)
        Получает запись из репозитория на основе данных из JWT.
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo: UserRepository = user_repo

    async def sign_in(self, form_data: OAuth2PasswordRequestForm) -> TokenResponse:
        """Метод аутентификации.

        Получает данные аутентификации пользователя (имя пользователя, пароль),
        выполняет аутентификацию и возвращает JWT.

        Parameters
        ----------
        form_data : OAuth2PasswordRequestForm
            Данные аутентификации пользователя.

        Returns
        -------
        response : TokenResponse
            Модель ответа сервера с вложенной парой JWT.
        """
        user = await self.user_repo.get_user_by_username(form_data.username)

        # проверка на существование пользователя и соответствие пароля
        if not (user and verify(form_data.password, user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenResponse(**await self._get_jwt_pair(user), token_type="bearer")

    async def sign_up(self, sign_up_data: SignUpRequest) -> StandardResponse:
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
            await self.user_repo.rollback()

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

    async def refresh(self, user: User) -> TokenResponse:
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

    async def validate_access_token(self, access_token: str) -> User:
        """Метод валидации токена доступа.

        Получает JSON Web Token (JWT) в качестве ввода, декодирует его и проверяет,
        существует ли пользователь в репозитории. Возвращает модель записи пользователя.

        Parameters
        ----------
        access_token : AnyStr
            JSON Web Token, токен доступа.

        Returns
        -------
        user : User
            Объект пользователя.
        """
        return await self._get_user_from_token(access_token)

    async def validate_refresh_token(self, refresh_token: str) -> User:
        """Метод валидации токена обновления.

        Получает refresh_token пользователя, декодирует его,
        проверяет на совпадение в репозитории.

        Parameters
        ----------
        refresh_token : str
            JSON Web Token, токен обновления.

        Returns
        -------
        user : User
            Объект пользователя.
        """
        user = await self._get_user_from_token(refresh_token)

        if user.refresh_token != refresh_token:
            raise credentials_exception

        return user

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
            await self.user_repo.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect request.",
            )

        return tokens

    async def _get_user_from_token(self, token: str) -> User:
        """Метод получения записи пользователя с помощью данных из JWT.

        Получает JWT в качестве ввода, декодирует его и проверяет, существует ли пользователь в репозитории.
        Возвращает модель записи пользователя.

        Parameters
        ----------
        token : str
            JSON Web Token.

        Returns
        -------
        user : User
            Модель записи пользователя.
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

        if (user := await self.user_repo.get_user_by_username(username)) is None:
            raise credentials_exception

        try:
            await self.user_repo.commit()
        except IntegrityError:
            await self.user_repo.rollback()

            raise credentials_exception

        return user
