from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import Uuid, String

from app.database.tables.base import Base

if TYPE_CHECKING:
    from app.database.tables.entities import Group, Client


class Relationship(Base):
    __tablename__ = "relationship"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="relationship_pkey"),
        ForeignKeyConstraint(
            ["group_id"],
            ["group.id"],
            name="relationship_group_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="relationship_client_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями о связях между клиентами.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    group_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    client_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    role: Mapped[str] = mapped_column(String(256), nullable=False)

    group: Mapped["Group"] = relationship("Group", back_populates="relationships")
    client: Mapped["Client"] = relationship("Client", back_populates="relationships")

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"group_id={self.group_id!r}, "
            f"client_id={self.client_id!r}, "
            f"role={self.role!r}"
            f")>"
        )
