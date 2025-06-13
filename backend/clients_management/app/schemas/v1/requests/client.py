from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class AddClientRequest(BaseModel):
    """Схема запроса на создание клиента.

    Используется в качестве схемы представления запроса на создание клиента.

    Attributes
    ----------
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
    """

    name: str = Field(examples=["Пётр"])
    surname: str = Field(examples=["Семёнов"])
    patronymic: str = Field(examples=["Олегович"])
    sex: bool = Field(examples=[True])
    email: EmailStr | None = Field(default=None, examples=["petr.semyonov@mail.ru"])
    phone: PhoneNumber = Field(examples=["+7 999 138-21-29"])
    photo_url: str | None = Field(default=None, examples=["/photos/aWuTrnX5AGv.jpg"])
