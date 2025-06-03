from typing import List

from pydantic import Field

from app.schemas.client import CompactClientModel, ClientModel
from .standard import StandardResponse


class ClientResponse(StandardResponse):
    """Модель ответа API, содержащая список клиентов и стандартные метаданные.

    Наследуется от StandardResponse, добавляя поле с массивом клиентов.
    Используется для всех ответов API, которые возвращают список клиентов.

    Attributes
    ----------
    client : ClientModel
        Список объектов клиентов.

    Notes
    -----
    - Наследует все стандартные поля из StandardResponse (например, status, message, error)
    - Гарантирует единообразную структуру ответов API
    - Позволяет добавлять метаданные (пагинацию, фильтры) в стандартные поля
    """

    client: ClientModel = Field()


class ClientsResponse(StandardResponse):
    """Модель ответа API, содержащая список клиентов и стандартные метаданные.

    Наследуется от StandardResponse, добавляя поле с массивом клиентов.
    Используется для всех ответов API, которые возвращают список клиентов.

    Attributes
    ----------
    clients : List[CompactClientModel]
        Список объектов клиентов, где каждый элемент соответствует модели CompactClient.
        Может быть пустым, если клиенты не найдены.

    Notes
    -----
    - Наследует все стандартные поля из StandardResponse (например, status, message, error)
    - Гарантирует единообразную структуру ответов API
    - Позволяет добавлять метаданные (пагинацию, фильтры) в стандартные поля
    """

    clients: List[CompactClientModel] = Field()
