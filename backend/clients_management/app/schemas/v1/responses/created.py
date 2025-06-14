from uuid import UUID

from fastapi import status
from pydantic import Field

from .standard import StandardResponse


class CreatedResponse(StandardResponse):
    """Ответ, возвращаемый после успешного создания ресурса.

    Атрибут `code` переопределён из родительского класса `StandardResponse` и по умолчанию равен 201 (Created).
    Помимо стандартных полей, содержит идентификатор созданного ресурса.

    Attributes
    ----------
    code : int, optional
        HTTP-код ответа. По умолчанию `201` — ресурс успешно создан.
    id : UUID
        Уникальный идентификатор созданного ресурса.
    """

    code: int = Field(
        default=status.HTTP_201_CREATED, examples=[status.HTTP_201_CREATED]
    )
    id: UUID = Field(examples=["e781a46e-17b7-4a88-a956-ebc9c4e5f0ef"])
