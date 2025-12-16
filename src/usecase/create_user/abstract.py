from abc import ABC, abstractmethod

from api.v1.user.models import CreateUserSchema


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CreateUserSchema):
        ...
