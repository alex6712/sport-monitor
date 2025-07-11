from datetime import date
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.schemas.group import CompactGroupModel
from app.schemas.season_ticket import SeasonTicketModel


class _BaseClientModel(BaseModel):
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
    sex : bool
        Пол клиента.
    email : EmailStr
        Электронная почта клиента. Проходит строгую валидацию формата email.
    phone : PhoneNumber
        Номер телефона в международном формате E.164. Автоматически форматируется.
    photo_url : str
        Путь к фотографии клиента. Может быть относительным (для локальных файлов)
        или абсолютным URL.

    Notes
    -----
    - Значение True в атрибуте `sex` означает мужской пол, False - женский.
    - Все строковые поля автоматически триммируются (удаляются пробелы по краям).
    - Для email используется валидация через EmailStr (должен содержать @ и домен).
    - PhoneNumber автоматически нормализует номер (удаляет пробелы, скобки и т.д.).
    - Для UUID используется версия 4 (случайные UUID).
    """

    id: UUID = Field(examples=["7e242293-b06e-4f99-85b4-355e594b33a9"])
    name: str = Field(examples=["Пётр"])
    surname: str = Field(examples=["Семёнов"])
    patronymic: str = Field(examples=["Олегович"])
    sex: bool = Field(examples=[True])
    email: EmailStr | None = Field(examples=["petr.semyonov@mail.ru"])
    phone: PhoneNumber = Field(examples=["+7 999 138-21-29"])
    photo_url: str | None = Field(examples=["/photos/aWuTrnX5AGv.jpg"])


class CompactClientModel(_BaseClientModel):
    """Сокращённая модель данных клиента для отображения в списках и UI-таблицах.

    Наследует все базовые поля от _BaseClient и добавляет служебную информацию
    для быстрого анализа статуса клиента.

    Attributes
    ----------
    season_ticket_type : str | None
        Тип текущего абонемента клиента. Если в данный момент у клиента
        нет абонемента (просрочен или не был куплен), возвращается None.
    is_violator : bool
        Флаг наличия нарушений у клиента.
    last_visit : date
        Дата последнего посещения в формате YYYY-MM-DD.
        Может быть None, если клиент ещё не посещал заведение.

    Notes
    -----
    - Используется в endpoints, возвращающих списки клиентов.
    - Оптимизирована для отображения в таблицах (меньше полей, чем в полной модели).
    """

    season_ticket_type: str | None = Field(examples=["семейный"])
    is_violator: bool = Field(examples=[True])
    last_visit: date | None = Field(examples=["2025-06-02"])


class ClientModel(_BaseClientModel):
    """Модель данных клиента, представляющая сущность из базы данных.

    Модель описывает все данные клиента, включая контактную информацию,
    ссылку на фотографию, информацию об абонементе, группах клиента и т.д.
    Все поля обязательны для заполнения.

    Attributes
    ----------
    groups : List[CompactGroupModel]
        Список всех групп, в которых состоит клиент. В сокращённом формате.
    season_tickets : List[SeasonTicketModel]
        Полная информация обо всех абонементах клиента.
    """

    groups: List[CompactGroupModel] = Field()
    season_tickets: List[SeasonTicketModel] = Field()
