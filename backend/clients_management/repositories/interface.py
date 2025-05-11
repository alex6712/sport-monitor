from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryInterface:
    """Интерфейс репозитория.

    Реализация паттерна Репозиторий. Является интерфейсом доступа к данным (DAO).

    Attributes
    ----------
    session : AsyncSession
        Объект асинхронной сессии запроса.

    Methods
    -------
    commit()
        Прокси метода ``session.commit()``.
    rollback()
        Прокси метода ``session.rollback()``.
    """

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def commit(self):
        """Прокси метода ``session.commit()``.

        Проксирует вызов метода ``commit`` у объекта текущей сессии.
        """
        await self.session.commit()

    async def rollback(self):
        """Прокси метода ``session.rollback()``.

        Проксирует вызов метода ``rollback`` у объекта текущей сессии.
        """
        await self.session.rollback()
