import secrets
import hashlib

from datetime import datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.models import TokenSchema
from api.v1.user.models import UserSchema
from infrastructure.databases.postgresql.models import Token


class PostgreSQLTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, user: UserSchema) -> TokenSchema:
        # author = Token(
        #     user_id=payload.user_id,
        #     full_name=payload.full_name,
        # )

        algorithm = hashlib.sha256()

        access_token = secrets.token_urlsafe(56)
        refresh_token = secrets.token_urlsafe(56)

        algorithm.update(access_token.encode('utf-8'))
        hex_access_token = algorithm.hexdigest()

        algorithm.update(refresh_token.encode('utf-8'))
        hex_refresh_token = algorithm.hexdigest()

        access_token_expires_in = datetime.now() + timedelta(minutes=15)
        refresh_token_expires_in = datetime.now() + timedelta(hours=24)

        token = Token(
            user_id=user.id,
            access_token=hex_access_token,
            refresh_token=hex_refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in,
        )

        self._session.add(token)
        await self._session.flush()
        schema = TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in
        )
        return schema
