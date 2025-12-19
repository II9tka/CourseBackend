from api.v1.auth.models import UserLoginSchema

from .abstract import AbstractCreateTokenUseCase


class PostgreSQLCreateTokenUseCase(AbstractCreateTokenUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: UserLoginSchema):
        async with self._uow as uow_:
            user = await uow_.user_repository.get(schema)
            token = await uow_.repository.create(user)
        return token
