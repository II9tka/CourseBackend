import secrets
import datetime

from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.models import TokenSchema, RefreshTokenSchema
from api.v1.user.models import UserSchema
from infrastructure.databases.postgresql.models import Token, User
from infrastructure.repositories.postgresql.token.crypto import hash_token


class PostgreSQLTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, user: UserSchema) -> TokenSchema:
        access_token = secrets.token_urlsafe(56)
        refresh_token = secrets.token_urlsafe(56)

        hex_access_token = hash_token(access_token)
        hex_refresh_token = hash_token(refresh_token)

        access_token_expires_in = datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
        refresh_token_expires_in = datetime.datetime.now(datetime.UTC) + timedelta(hours=24)

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

    async def delete(self, token: Token) -> None:
        await self._session.delete(token)
        await self._session.flush()

    async def refresh(self, schema: RefreshTokenSchema) -> TokenSchema:
        hex_refresh_token = hash_token(schema.refresh_token)

        query = select(Token).where(Token.refresh_token == hex_refresh_token)
        result = await self._session.execute(query)

        token = result.scalar_one_or_none()

        if not token:
            raise ...

        access_token = secrets.token_urlsafe(56)
        refresh_token = secrets.token_urlsafe(56)

        hex_access_token = hash_token(access_token)
        hex_refresh_token = hash_token(refresh_token)

        access_token_expires_in = datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
        refresh_token_expires_in = datetime.datetime.now(datetime.UTC) + timedelta(hours=24)

        new_token = Token(
            user_id=token.user_id,
            access_token=hex_access_token,
            refresh_token=hex_refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in,
        )

        self._session.add(new_token)

        await self._session.flush()
        await self.delete(token)

        schema = TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in
        )
        return schema

    async def get_user(self, access_token: str) -> UserSchema:
        hex_access_token = hash_token(access_token)

        query = select(User).join(Token, User.id==Token.user_id).where(
            Token.access_token == hex_access_token
        )
        result = await self._session.execute(query)

        user = result.scalar_one_or_none()

        if not user:
            ...

        return UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            biography=user.biography,
            full_name=user.full_name,
        )
