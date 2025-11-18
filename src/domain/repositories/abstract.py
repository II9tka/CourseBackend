from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")
TCreateDTO = TypeVar("TCreateDTO")
TUpdateDTO = TypeVar("TUpdateDTO")


class AbstractRepository(Generic[TEntity, TId, TCreateDTO, TUpdateDTO], ABC):
    """
    Общий абстрактный репозиторий.

    Не знает ни про Item, ни про конкретные DTO —
    только про типы, заданные дженериками.
    """

    @abstractmethod
    def get(self, entity_id: TId) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def list(self, *, limit: int = 100, offset: int = 0) -> List[TEntity]:
        raise NotImplementedError

    @abstractmethod
    def create(self, dto: TCreateDTO) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: TId, dto: TUpdateDTO) -> TEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: TId) -> None:
        raise NotImplementedError
