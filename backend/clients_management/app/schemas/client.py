from datetime import date
from typing import List, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

if TYPE_CHECKING:
    from app.schemas.group import CompactGroup


class _BaseClient(BaseModel):
    """Базовый класс модели клиента, содержащий общие поля для всех производных моделей.

    Attributes
    ----------
    id : UUID
        Уникальный идентификатор клиента в системе. Формат RFC 4122.
    name : str
        Имя клиента.
    surname : str
        Фамилия клиента.
    patronymic : str
        Отчество клиента.
    email : EmailStr
        Электронная почта клиента. Проходит строгую валидацию формата email.
    phone : PhoneNumber
        Номер телефона в международном формате E.164. Автоматически форматируется.
    photo_url : str
        Путь к фотографии клиента. Может быть относительным (для локальных файлов)
        или абсолютным URL.

    Notes
    -----
    - Все строковые поля автоматически триммируются (удаляются пробелы по краям).
    - Для email используется валидация через EmailStr (должен содержать @ и домен).
    - PhoneNumber автоматически нормализует номер (удаляет пробелы, скобки и т.д.).
    - Для UUID используется версия 4 (случайные UUID).
    """

    id: UUID = Field(examples=["7e242293-b06e-4f99-85b4-355e594b33a9"])
    name: str = Field(examples=["Пётр"])
    surname: str = Field(examples=["Семёнов"])
    patronymic: str = Field(examples=["Олегович"])
    email: EmailStr = Field(examples=["petr.semyonov@mail.ru"])
    phone: PhoneNumber = Field(examples=["+7 999 138-21-29"])
    photo_url: str = Field(examples=["/photos/aWuTrnX5AGv.jpg"])


class CompactClient(_BaseClient):
    """Сокращённая модель данных клиента для отображения в списках и UI-таблицах.

    Наследует все базовые поля от _BaseClient и добавляет служебную информацию
    для быстрого анализа статуса клиента.

    Attributes
    ----------
    season_ticket_type : str
        Тип абонемента клиента.
    violator : bool
        Флаг наличия нарушений у клиента.
    last_visit : date
        Дата последнего посещения в формате YYYY-MM-DD.
        Может быть None, если клиент ещё не посещал заведение.

    Notes
    -----
    - Используется в endpoints, возвращающих списки клиентов.
    - Оптимизирована для отображения в таблицах (меньше полей, чем в полной модели).
    """

    season_ticket_type: str = Field(examples=["семейный"])
    violator: bool = Field(examples=[True])
    last_visit: date = Field(examples=["2025-06-02"])


class Client(_BaseClient):
    """Модель данных клиента, представляющая сущность из базы данных.

    Модель описывает все данные клиента, включая контактную информацию,
    ссылку на фотографию, информацию об абонементе, группах клиента и т.д.
    Все поля обязательны для заполнения.

    Attributes
    ----------

    """

    groups: List[CompactGroup] = Field()
