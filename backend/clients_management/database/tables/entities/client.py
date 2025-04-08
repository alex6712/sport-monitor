from uuid import UUID, uuid4

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.types import String, Uuid

from database.tables.base import Base


class Client(Base):
    __tablename__ = "client"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="client_pkey"),
        {
            "comment": "Таблица с записями о клиентах.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid, default=uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    surname: Mapped[str] = mapped_column(String(256), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(256), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(256), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"surname={self.surname!r}, "
            f"patronymic={self.patronymic!r}, "
            f"photo_url={self.photo_url!r}"
            f")>"
        )
