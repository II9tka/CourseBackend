from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from ..base import Base


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[Optional[str]] = mapped_column(String(300))
