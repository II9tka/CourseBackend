from typing import Dict, Optional, List

from domain.item.models import Item, ItemCreateDTO, ItemUpdateDTO
from domain.item.repository import AbstractItemRepository
from domain.item.exceptions import ItemNotFoundError


class InMemoryItemRepository(AbstractItemRepository):
    """In-memory реализация, псевдо-таблица {id: Item}."""

    def __init__(self, storage: Optional[Dict[int, Item]] = None) -> None:
        self._storage: Dict[int, Item] = storage.copy() if storage else {}

    # ----- реализации AbstractRepository -----

    def get(self, entity_id: int) -> Item:
        try:
            return self._storage[entity_id]
        except KeyError:
            raise ItemNotFoundError(entity_id)

    def list(self, *, limit: int = 100, offset: int = 0) -> List[Item]:
        items = list(self._storage.values())
        return items[offset: offset + limit]

    def create(self, dto: ItemCreateDTO) -> Item:
        if self._storage:
            last_id = list(self._storage)[-1]
            next_id = last_id + 1
        else:
            next_id = 1

        item = Item(
            id=next_id,
            title=dto.title,
            description=dto.description,
        )
        self._storage[next_id] = item
        return item

    def update(self, entity_id: int, dto: ItemUpdateDTO) -> Item:
        if entity_id not in self._storage:
            raise ItemNotFoundError(entity_id)

        existing = self._storage[entity_id]
        updated = Item(
            id=existing.id,
            title=dto.title if dto.title is not None else existing.title,
            description=dto.description if dto.description is not None else existing.description,
        )
        self._storage[entity_id] = updated
        return updated

    def delete(self, entity_id: int) -> None:
        if entity_id not in self._storage:
            raise ItemNotFoundError(entity_id)

        del self._storage[entity_id]
