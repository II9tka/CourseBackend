from abc import ABC, abstractmethod

from api.v1.auth.models import UserLoginSchema, RefreshTokenSchema, TokenSchema


class AbstractRefreshTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: RefreshTokenSchema) -> TokenSchema:
        ...
