from uuid import UUID, uuid4

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.types import Uuid, String

from database.tables.base import Base


class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_pkey"),
        UniqueConstraint("username", name="user_username_uk"),
        UniqueConstraint("email", name="user_email_uk"),
        {
            "comment": "Таблица с записями о пользователях.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid, default=uuid4)
    username: Mapped[str] = mapped_column(String(256), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=True)
    email: Mapped[str] = mapped_column(String(256), nullable=True)
    refresh_token: Mapped[str] = mapped_column(
        String(256), nullable=True, comment="Токен обновления токена доступа."
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"username={self.username!r}, "
            f"password={self.password!r}, "
            f"email={self.email!r}, "
            f"refresh_token={self.refresh_token!r}"
            f")>"
        )
