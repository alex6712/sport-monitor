import uvicorn

from core.config import Settings, get_settings

if __name__ == "__main__":
    settings: Settings = get_settings()

    if settings.DEV_MODE:
        swagger_url: str = f"http://{settings.DOMAIN}:{settings.BACKEND_PORT}/docs"
        print(f"Swagger UI URL: \033[97m{swagger_url}\033[0m")

    uvicorn.run(
        app="main:clients_management",
        host=settings.DOMAIN,
        port=settings.BACKEND_PORT,
        reload=settings.DEV_MODE,
    )
