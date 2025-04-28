from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    """Схема объекта пользователя с паролем.

    Используется в качестве представления информации о пользователе, включая его пароль.

    Attributes
    ----------
    username : str
        Логин пользователя.
    password : str
        Пароль пользователя.
    email : EmailStr
        Адрес электронной почты пользователя.
    """

    username: str = Field(examples=["someone"])
    password: str = Field(examples=["password"])
    email: EmailStr = Field(default=None, examples=["someone@post.domen"])
