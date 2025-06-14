from uuid import UUID

from pydantic import BaseModel, Field


class VisitRequest(BaseModel):
    """Схема запроса на создание записи о посещении.

    Используется в качестве схемы представления запроса на создание записи о посещении.

    Attributes
    ----------
    client_id : UUID
        UUID клиента, который посещает зал.
    box : int
        Номер ящика, который использует клиент во время посещения.
    """

    client_id: UUID = Field(examples=["8e1b38e9-b559-9f67-a2e8-a1839ee1d6a1"])
    box: int = Field(examples=[56])
