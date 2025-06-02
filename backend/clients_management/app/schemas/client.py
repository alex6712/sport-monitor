from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class Client(BaseModel):
    """Модель данных клиента, представляющая сущность из базы данных.

    Модель описывает основные персональные данные клиента, включая контактную информацию
    и ссылку на фотографию. Все поля обязательны для заполнения.

    Attributes
    ----------
    id : UUID
        Уникальный идентификатор клиента в системе.
    name : str
        Имя клиента. Должно содержать только буквы.
    surname : str
        Фамилия клиента. Должна содержать только буквы.
    patronymic : str
        Отчество клиента. Должно содержать только буквы.
    email : EmailStr
        Электронная почта клиента. Должна соответствовать стандартному формату email.
    phone : PhoneNumber
        Номер телефона клиента в международном формате.
    photo_url : str
        URL-адрес фотографии клиента. Может быть относительным путем на сервере
        или полным URL, если фотография хранится на внешнем ресурсе.
        Пример: "/photos/aWuTrnX5AGv.jpg"

    Notes
    -----
    - Все строковые поля автоматически проверяются на соответствие типам данных.
    - Email и телефон проходят дополнительную валидацию формата.
    - Для UUID используется стандартный формат RFC 4122.
    """

    id: UUID = Field(examples=["7e242293-b06e-4f99-85b4-355e594b33a9"])
    name: str = Field(examples=["Пётр"])
    surname: str = Field(examples=["Семёнов"])
    patronymic: str = Field(examples=["Олегович"])
    email: EmailStr = Field(examples=["petr.semyonov@mail.ru"])
    phone: PhoneNumber = Field(examples=["+7 999 138-21-29"])
    photo_url: str = Field(examples=["/photos/aWuTrnX5AGv.jpg"])
