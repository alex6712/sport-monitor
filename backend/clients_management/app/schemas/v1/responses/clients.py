from typing import List

from pydantic import Field

from .standard import StandardResponse
from app.schemas.client import Client


class ClientsResponse(StandardResponse):
    """Модель ответа API, содержащая список клиентов и стандартные метаданные.

    Наследуется от StandardResponse, добавляя поле с массивом клиентов.
    Используется для всех ответов API, которые возвращают список клиентов.

    Attributes
    ----------
    clients : List[Client]
        Список объектов клиентов, где каждый элемент соответствует модели Client.
        Может быть пустым, если клиенты не найдены.

    Notes
    -----
    - Наследует все стандартные поля из StandardResponse (например, status, message, error)
    - Гарантирует единообразную структуру ответов API
    - Позволяет добавлять метаданные (пагинацию, фильтры) в стандартные поля
    """
    clients: List[Client] = Field()
