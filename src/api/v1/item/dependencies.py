from domain.item.repository import AbstractItemRepository
from infrastructure.repositories.inmemory.item import InMemoryItemRepository

_item_repo = InMemoryItemRepository()


def get_item_repo() -> AbstractItemRepository:
    return _item_repo
