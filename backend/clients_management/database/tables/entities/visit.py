from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import DateTime, Integer, Uuid

from database.tables.base import Base

if TYPE_CHECKING:
    from database.tables.entities import Client


class Visit(Base):
    __tablename__ = "visit"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="visit_pkey"),
        ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="visit_client_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями о посещениях.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    client_id: Mapped[UUID] = mapped_column(Uuid())
    visit_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    visit_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    box: Mapped[int] = mapped_column(Integer(), nullable=False)

    client: Mapped["Client"] = relationship("Client", back_populates="visits")

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"client_id={self.client_id!r}, "
            f"visit_start={self.visit_start!r}, "
            f"visit_end={self.visit_end!r}, "
            f"box={self.box!r}"
            f")>"
        )
