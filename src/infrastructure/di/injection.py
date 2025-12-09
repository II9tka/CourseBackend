from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repositories.postgresql.uow import PostgreSQLAuthorUnitOfWork


def build_author_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAuthorUnitOfWork:
    return Container.author_uow_factory(session=session)