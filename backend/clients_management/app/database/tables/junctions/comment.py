from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.types import String, Uuid

from app.database.tables.base import Base

if TYPE_CHECKING:
    from app.database.tables.entities import Client, User


class Comment(Base):
    __tablename__ = "comment"

    __table_args__ = (
        PrimaryKeyConstraint("id", name="comment_pkey"),
        ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="comment_user_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["client_id"],
            ["client.id"],
            name="comment_client_id_fk",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        {
            "comment": "Таблица с записями о комментариях пользователей о клиентах.",
        },
    )

    id: Mapped[UUID] = mapped_column(Uuid(), default=uuid4)
    user_id: Mapped[UUID] = mapped_column(Uuid())
    client_id: Mapped[UUID] = mapped_column(Uuid())
    comment: Mapped[str] = mapped_column(String(1024), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    client: Mapped["Client"] = relationship("Client", back_populates="comments")

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"client_id={self.client_id!r}, "
            f"comment={self.comment!r}"
            f")>"
        )
