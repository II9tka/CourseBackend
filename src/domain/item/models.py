from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Item:
    id: int
    title: str
    description: str


@dataclass(slots=True)
class ItemCreateDTO:
    title: str
    description: str


@dataclass(slots=True)
class ItemUpdateDTO:
    title: Optional[str] = None
    description: Optional[str] = None
