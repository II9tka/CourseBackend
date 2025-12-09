from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from ..base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    biography: Mapped[str] = mapped_column(String(1000))

    author: Mapped[Optional["Author"]] = relationship(back_populates="user")