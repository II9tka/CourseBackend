from abc import ABC

from domain.repositories.abstract import AbstractRepository

from .models import Item, ItemCreateDTO, ItemUpdateDTO
from .exceptions import ItemNotFoundError


class AbstractItemRepository(
    AbstractRepository[Item, int, ItemCreateDTO, ItemUpdateDTO],
    ABC,
):
    """
    Контракт репозитория для Item.

    Сейчас просто наследуем общий AbstractRepository.
    Если потом понадобятся доменные методы (find_by_title и т.п.) —
    добавить сюда.
    """

    # пример доменного метода на будущее:
    # @abstractmethod
    # def find_by_title(self, title: str) -> List[Item]:
    #     raise NotImplementedError
    ...
