from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.author.models import CreateUpdateAuthorSchema, AuthorSchema
from infrastructure.databases.postgresql.models import Author


class PostgreSQLAuthorRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CreateUpdateAuthorSchema) -> AuthorSchema:
        author = Author(
            user_id=payload.user_id,
            full_name=payload.full_name,
        )
        self._session.add(author)
        await self._session.flush()
        schema = AuthorSchema(
            id=author.id,
            full_name=author.full_name,
            user_id=author.user_id,
        )
        return schema

    async def get(self, author_id: int) -> AuthorSchema | None:
        author = await self._session.get(Author, author_id)

        if author is not None:
            author = AuthorSchema(
                id=author.id,
                full_name=author.full_name,
                user_id=author.user_id,
            )
        return author

    async def list(
        self,
        author_id: int | None = None,
        full_name: str | None = None,
        user_id: int | None = None,
    ):
        expression = []

        if author_id is not None:
            expression.append(and_(Author.id == author_id))
        if full_name is not None:
            expression.append(and_(Author.full_name.ilike(f'%{full_name}%')))
        if user_id is not None:
            expression.append(and_(Author.user_id == user_id))

        query = select(Author).where(*expression)

        result = await self._session.execute(query)
        scalars = result.scalars()

        return [AuthorSchema.model_validate(scalar, from_attributes=True) for scalar in scalars]




