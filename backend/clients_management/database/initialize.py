import asyncio

from asyncpg.exceptions import ConnectionDoesNotExistError
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from core.config import Settings, get_settings
from database.tables.base import Base


async def initialize():
    """Инициализация базы данных.

    Сбрасывает все таблицы, а затем воссоздает.
    Это удалит всю информацию из существующих таблиц, поэтому
    это очень небезопасная операция.

    Вот почему эта функция требует подтверждения суперпользователя.
    """
    settings: Settings = get_settings()

    engine: AsyncEngine = create_async_engine(
        url=settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    error = (
        "\n\033[91mWhile initializing database:"
        "\n\tFAIL:  {fail}"
        "\n\tCAUSE: {cause}"
        "\nContinuing without initializing...\033[0m\n"
    )

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        async with engine.begin() as conn:
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
    else:
        print("\n\033[92mDatabase initialized successfully.\033[0m\n")


if __name__ == "__main__":
    asyncio.run(initialize())
