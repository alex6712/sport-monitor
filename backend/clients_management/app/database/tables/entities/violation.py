from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import Uuid, String, DateTime

from app.database.tables.base import Base

if TYPE_CHECKING:
    from app.database.tables.entities import Client


class Violation(Base):
    __tablename__ = "violation"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="violation_pkey"),
        ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="violation_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями о нарушениях клиентов.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    detail: Mapped[str] = mapped_column(String(256), nullable=False)
    client_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    claimed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    client: Mapped["Client"] = relationship("Client", back_populates="violations")

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"detail={self.detail!r}, "
            f"client_id={self.client_id!r}, "
            f"claimed_at={self.claimed_at!r}"
            f")>"
        )
