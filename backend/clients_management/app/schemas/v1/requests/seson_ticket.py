from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class SeasonTicketRequest(BaseModel):
    """Схема запроса на создание абонемента.

    Используется в качестве схемы представления запроса на создание абонемента.

    Attributes
    ----------
    client_id : UUID
        UUID клиента, на которого оформлен абонемент.
    type : str
        Тип абонемента
    expires_at : str
        Срок действия абонемента (дата окончания).
    """

    client_id: UUID = Field(examples=["8e1b38e9-b559-9f67-a2e8-a1839ee1d6a1"])
    type: str = Field(examples=["семейный"])
    expires_at: datetime = Field(examples=["2025-06-02 12:32:11.000311+00:00"])
