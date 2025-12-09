from abc import ABC, abstractmethod

from api.v1.author.models import CreateUpdateAuthorSchema


class AbstractCreateAuthorUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CreateUpdateAuthorSchema):
        ...