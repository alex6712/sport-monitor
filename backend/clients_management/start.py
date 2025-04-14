import asyncio
import asyncpg

import uvicorn

from core.config import Settings, get_settings
from database import initialize

STACK_TRACE = set()


async def wait_for_db():
    global STACK_TRACE

    for _ in range(10):
        try:
            conn = await asyncpg.connect(settings.DATABASE_URL)
            await conn.close()
            return True
        except Exception as e:
            STACK_TRACE.add(str(e))
            await asyncio.sleep(2)
    return False


if __name__ == "__main__":
    settings: Settings = get_settings()

    if not asyncio.run(wait_for_db()):
        raise RuntimeError(f"Не удалось подключиться к БД. Ошибки: {STACK_TRACE}")

    if settings.INITIALIZE_DB:
        asyncio.run(initialize())

    print(
        f"Swagger UI URL: \033[97mhttp://{settings.DOMAIN}:{settings.BACKEND_PORT}/docs\033[0m"
    )

    uvicorn.run(
        app="main:clients_management",
        host=settings.DOMAIN,
        port=settings.BACKEND_PORT,
        reload=settings.DEV_MODE,
    )
