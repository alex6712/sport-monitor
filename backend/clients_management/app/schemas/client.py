from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class Client(BaseModel):
    """TODO: docstring"""

    id: UUID = Field(examples=["7e242293-b06e-4f99-85b4-355e594b33a9"])
    name: str = Field(examples=["Пётр"])
    surname: str = Field(examples=["Семёнов"])
    patronymic: str = Field(examples=["Олегович"])
    email: EmailStr = Field(examples=["petr.semyonov@mail.ru"])
    phone: PhoneNumber = Field(examples=["+7 999 138-21-29"])
    photo_url: str = Field(examples=["/photos/aWuTrnX5AGv.jpg"])
