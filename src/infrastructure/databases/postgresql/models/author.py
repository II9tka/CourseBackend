from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from ..base import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(128))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="author")
    books: Mapped[list["Book"]] = relationship(back_populates="author")

