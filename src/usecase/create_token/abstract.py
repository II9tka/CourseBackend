from abc import ABC, abstractmethod

from api.v1.auth.models import UserLoginSchema


class AbstractCreateTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: UserLoginSchema):
        ...
