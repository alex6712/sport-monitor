import uvicorn

from core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()

    uvicorn.run(
        app="main:clients_management",
        host=settings.DOMAIN,
        port=settings.BACKEND_PORT,
        reload=settings.DEV_MODE,
    )
