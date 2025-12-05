from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.uow import PostgreSQLAuthorUnitOfWork


def get_author_unit_of_work(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLAuthorUnitOfWork:
    return PostgreSQLAuthorUnitOfWork(session=session)