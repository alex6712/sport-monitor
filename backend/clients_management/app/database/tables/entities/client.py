from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import String, Uuid, Boolean

from app.database.tables.base import Base
from .season_ticket import SeasonTicket
from .transaction import Transaction

if TYPE_CHECKING:
    from app.database.tables.entities import (
        Group,
        Violation,
        Visit,
    )
    from app.database.tables.junctions import (
        Comment,
        Complaint,
        Relationship,
    )


class Client(Base):
    __tablename__ = "client"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="client_pkey"),
        {
            "comment": "Таблица с записями о клиентах.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    surname: Mapped[str] = mapped_column(String(256), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(256), nullable=False)
    sex: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(256), nullable=True)
    phone: Mapped[PhoneNumber] = mapped_column(String(32), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(256), nullable=False)

    relationships: Mapped[List["Relationship"]] = relationship(
        "Relationship", back_populates="client"
    )
    groups: Mapped[List["Group"]] = relationship(
        "Group",
        secondary="relationship",
        viewonly=True,
    )
    season_tickets: Mapped[List["SeasonTicket"]] = relationship(
        "SeasonTicket",
        back_populates="client",
        order_by=SeasonTicket.expires_at,
    )
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="client",
        order_by=Transaction.timestamp,
    )
    violations: Mapped[List["Violation"]] = relationship(
        "Violation", back_populates="client"
    )
    visits: Mapped[List["Visit"]] = relationship("Visit", back_populates="client")

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="client")
    complaints: Mapped[List["Complaint"]] = relationship(
        "Complaint", back_populates="client"
    )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"surname={self.surname!r}, "
            f"patronymic={self.patronymic!r}, "
            f"sex={self.sex!r}, "
            f"email={self.email!r}, "
            f"phone={self.phone!r}, "
            f"photo_url={self.photo_url!r}"
            f")>"
        )
