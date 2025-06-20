from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import DateTime, Uuid, String

from app.database.tables.base import Base

if TYPE_CHECKING:
    from app.database.tables.entities import Client


class SeasonTicket(Base):
    __tablename__ = "season_ticket"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="season_ticket_pkey"),
        ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="season_ticket_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями об абонементах клиентов.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    client_id: Mapped[UUID] = mapped_column(Uuid())
    type: Mapped[str] = mapped_column(String(256))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    client: Mapped["Client"] = relationship("Client", back_populates="season_tickets")

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"type={self.type!r}, "
            f"expires_at={self.expires_at!r}"
            f")>"
        )
