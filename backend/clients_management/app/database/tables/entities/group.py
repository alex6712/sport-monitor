from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import String, Uuid

from app.database.tables.base import Base

if TYPE_CHECKING:
    from app.database.tables.entities import Client
    from app.database.tables.junctions import Relationship


class Group(Base):
    __tablename__ = "group"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="group_pkey"),
        {
            "comment": "Таблица с записями о группах клиентов.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    type: Mapped[str] = mapped_column(String(256), nullable=False)

    relationships: Mapped[List["Relationship"]] = relationship(
        "Relationship", back_populates="group"
    )
    clients: Mapped[List["Client"]] = relationship(
        "Client",
        secondary="relationship",
        viewonly=True,
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"type={self.type!r}"
            f")>"
        )
