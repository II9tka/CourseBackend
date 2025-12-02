from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.author.models import CreateUpdateAuthorSchema, AuthorSchema
from databases.postgresql.models import Author
from databases.postgresql.session_manager import sessionmanager


class PostgreSQLAuthorRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CreateUpdateAuthorSchema):
        author = Author(
            user_id=payload.user_id,
            full_name=payload.full_name,
        )
        self._session.add(author)
        await self._session.flush()
        return AuthorSchema(
            id=author.id,
            full_name=author.full_name,
            user_id=author.user_id,
        )