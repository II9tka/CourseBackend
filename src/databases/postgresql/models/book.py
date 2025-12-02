from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, ForeignKey

from utils.enums import Genre
from ..base import Base

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[Optional[str]] = mapped_column(String(300))
    genre: Mapped[Genre] = mapped_column(Enum(Genre), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))