from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1 import api_v1_router
from app.core.config import Settings, get_settings

settings: Settings = get_settings()

tags_metadata = [
    {
        "name": "root",
        "description": "Получение информации о **приложении**.",
    },
    {
        "name": "authorization",
        "description": "Операции **регистрации** и **аутентификации**.",
    },
    {
        "name": "clients",
        "description": "Операции с **клиентами**: _добавление_, _удаление_, _редактирование_.",
    },
    {
        "name": "season_tickets",
        "description": "Операции с **абонементами**: _добавление_, _удаление_, _редактирование_.",
    },
    {
        "name": "visits",
        "description": "Операции с **посещениями**: _добавление_, _удаление_, _редактирование_.",
    },
]

clients_management = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    summary=settings.APP_SUMMARY,
    contact={
        "name": settings.ADMIN_NAME,
        "email": settings.ADMIN_EMAIL,
    },
    openapi_tags=tags_metadata,
)

clients_management.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients_management.include_router(api_v1_router)
