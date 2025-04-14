import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from api.v1.dependencies import get_session
from core.config import Settings, get_settings
from main import clients_management
from tests.override import override_get_session, override_initialize

settings: Settings = get_settings()


@pytest_asyncio.fixture
async def async_client():
    await override_initialize()

    clients_management.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=clients_management),
        base_url=f"http://{settings.DOMAIN}:{settings.BACKEND_PORT}/{settings.CURRENT_API_URL}",
    ) as client:
        yield client
