from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_token_unit_of_work
from infrastructure.repositories.postgresql.token import PostgreSQLTokenUnitOfWork

from usecase.create_token.implementation import PostgreSQLCreateTokenUseCase
from usecase.refresh_token.implementation import PostgreSQLRefreshTokenUseCase


def get_token_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLTokenUnitOfWork:
    return build_token_unit_of_work(session)


def create_token_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return PostgreSQLCreateTokenUseCase(uow=uow)


def refresh_token_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return PostgreSQLRefreshTokenUseCase(uow=uow)
