from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import Settings, get_settings

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
        yield session  # noqa
