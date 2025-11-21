from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from .session_manager import sessionmanager


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
