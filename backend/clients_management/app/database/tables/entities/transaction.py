from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import DateTime, Uuid, Float

from app.database.tables.base import Base

if TYPE_CHECKING:
    from app.database.tables.entities import Client


class Transaction(Base):
    __tablename__ = "transaction"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="transaction_pkey"),
        ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="transaction_client_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями о транзакциях клиентов.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    client_id: Mapped[UUID] = mapped_column(Uuid())
    amount: Mapped[float] = mapped_column(Float())
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    client: Mapped["Client"] = relationship("Client", back_populates="transactions")

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"client_id={self.client_id!r}, "
            f"amount={self.amount!r}, "
            f"timestamp={self.timestamp!r}"
            f")>"
        )
