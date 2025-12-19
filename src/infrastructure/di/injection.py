from sqlalchemy.ext.asyncio import AsyncSession

from container import Container

from infrastructure.repositories.postgresql.author import PostgreSQLAuthorUnitOfWork
from infrastructure.repositories.postgresql.user import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgresql.token import PostgreSQLTokenUnitOfWork


def build_author_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLAuthorUnitOfWork:
    return Container.author_uow_factory(session=session)


def build_user_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLUserUnitOfWork:
    return Container.user_uow_factory(session=session)


def build_token_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLTokenUnitOfWork:
    return Container.token_uow_factory(session=session)
