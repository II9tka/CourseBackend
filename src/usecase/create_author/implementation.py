from api.v1.author.models import CreateUpdateAuthorSchema
from .abstract import AbstractCreateAuthorUseCase


class PostgreSQLCreateAuthorUseCase(AbstractCreateAuthorUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateUpdateAuthorSchema):
        async with self._uow as uow_:

            author = await uow_.repository.create(schema)

        return author
