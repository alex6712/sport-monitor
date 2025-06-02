from typing import List, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.client import CompactClientModel


class _BaseGroupModel(BaseModel):
    """Базовый класс модели группы, содержащий общие поля для всех производных моделей.

    Attributes
    ----------
    id : UUID
        Уникальный идентификатор группы в системе. Формат RFC 4122.
    type : str
        Тип группы. Определяет правила взаимодействия с группой.

    Notes
    -----
    - Все строковые поля автоматически триммируются (удаляются пробелы по краям).
    """

    id: UUID = Field(examples=["8e1b38e9-d429-4546-a2e8-a183f2e1d6a1"])
    type: str = Field(examples=["семья"])


class CompactGroupModel(BaseModel):
    """Сокращённая модель группы для отображения в списках и UI-таблицах.

    Содержит минимально необходимые данные для идентификации группы и
    отображения в интерфейсах, где не требуется детальная информация о клиентах.

    Attributes
    ----------
    quantity : int
        Текущее количество участников в группе.

    Notes
    -----
    - Используется в endpoints, возвращающих списки групп без детализации.
    - quantity автоматически пересчитывается при изменении состава группы.
    """

    quantity: int = Field(examples=[5])


class GroupModel(_BaseGroupModel):
    """Полная модель группы с сокращённой информацией о входящих в неё клиентах.

    Наследует все поля от `_BaseGroup` и добавляет список клиентов группы
    в сокращённом формате (CompactClient).

    Attributes
    ----------
    clients : List[CompactClientModel]
        Список клиентов, входящих в группу. Каждый клиент представлен
        в сокращённом формате CompactClient.

    Notes
    -----
    - Используется при запросе детальной информации о конкретной группе.
    - Количество клиентов всегда соответствует полю quantity.
    """

    clients: List["CompactClientModel"] = Field()
