from asyncpg.exceptions import ConnectionDoesNotExistError
from sqlalchemy.exc import ProgrammingError

from database import Base
from tests.override import test_engine


async def override_initialize():
    """Инициализирует тестовую базу данных.

    Инициализирует тестовую in-memory SQLite базу данных для изоляции
    тестов.

    Эта функция не требует подтверждения суперпользователя.
    """
    error = (
        "\n\033[91mWhile initializing database:"
        "\n\tFAIL:  {fail}"
        "\n\tCAUSE: {cause}"
        "\nContinuing without initializing...\033[0m\n"
    )

    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except ConnectionDoesNotExistError:
        print(
            error.format(
                fail="Unable to establish a connection.",
                cause="Incorrect password or username.",
            )
        )
    except ProgrammingError:
        print(
            error.format(
                fail="Unable to establish a connection.",
                cause="User is not the superuser.",
            )
        )
