from functools import lru_cache
from os.path import abspath
from typing import List

from pydantic import EmailStr, IPvAnyAddress, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    """Config project class.

    Used `pydantic`_ + `python-dotenv`_ to look up application settings described in .env.

    .. _`pydantic`:
        https://docs.pydantic.dev/
    .. _`python-dotenv`:
        https://pypi.org/project/python-dotenv/

    See Also
    --------
    pydantic
    python-dotenv

    Attributes
    ----------
    APP_NAME : str
        The name of the application.
    APP_VERSION : str
        The current version of the application.
    APP_DESCRIPTION : str
        Full description of the application.
    APP_SUMMARY : str
        Brief description of the application.
    ADMIN_NAME : str
        Name of the person responsible.
    ADMIN_EMAIL : EmailStr
        Email address to contact the person in charge.
    DEV_MODE : bool
        Development mode.
    INITIALIZE_DB : bool
        Recreate the DB.
    BACKEND_CORS_ORIGINS : List[str]
        List of sources for CORS Middleware.
    DOMAIN : str` | `IPvAnyAddress
        The IP of the domain where the application is located.
    BACKEND_PORT : int
        Application port.
    DATABASE_USER : str
        The database user to connect to.
    DATABASE_PASSWORD : str
        User password to connect to the database.
    DATABASE_PORT : int
        Database port.
    CURRENT_API_URL : int
        Current API version URL.
    DATABASE_NAME : str
        Database name.
    DATABASE_URL : PostgresDsn
        Connection string (link) to the database.
    TEST_DATABASE_URL : str
        Строка подключения к тестовой базе данных.
    JWT_SECRET_KEY : str
        The secret key to encode the JSON Web Token.
    JWT_ALGORITHM : str
        JWT encoding algorithm.
    ACCESS_TOKEN_LIFETIME_MINUTES : int
        Access token lifetime in minutes.
    REFRESH_TOKEN_LIFETIME_DAYS : int
        Refresh token lifetime in days.
    """

    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    APP_SUMMARY: str

    ADMIN_NAME: str
    ADMIN_EMAIL: EmailStr

    DEV_MODE: bool

    INITIALIZE_DB: bool

    BACKEND_CORS_ORIGINS: List[str]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")  # noqa
    @classmethod
    def assemble_cors_origins(cls, value: List[str] | str) -> List[str] | str:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]

        if isinstance(value, (list, str)):
            return value

        raise ValueError(value)

    DOMAIN: str | IPvAnyAddress

    BACKEND_PORT: int

    CURRENT_API_URL: str

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    DATABASE_URL: str
    TEST_DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int
    REFRESH_TOKEN_LIFETIME_DAYS: int

    model_config = SettingsConfigDict(
        env_file=abspath(".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        enable_decoding=False,
    )


@lru_cache
def get_settings() -> Settings:
    print(abspath(".env"))
    with open(abspath(".env"), "r", encoding="utf-8") as f:
        print(f.read())
    return Settings()
