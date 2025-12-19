from api.v1.auth.models import RefreshTokenSchema, TokenSchema

from .abstract import AbstractRefreshTokenUseCase


class PostgreSQLRefreshTokenUseCase(AbstractRefreshTokenUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: RefreshTokenSchema) -> TokenSchema:
        async with self._uow as uow_:
            token = await uow_.repository.refresh(schema)
        return token
