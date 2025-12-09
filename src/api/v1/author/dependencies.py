from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_author_unit_of_work
from infrastructure.repositories.postgresql.uow import PostgreSQLAuthorUnitOfWork

from usecase.create_author.implementation import PostgreSQLCreateAuthorUseCase


def get_author_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLAuthorUnitOfWork:
    return build_author_unit_of_work(session)


def create_author_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_author_unit_of_work(session)
    return PostgreSQLCreateAuthorUseCase(uow=uow)
