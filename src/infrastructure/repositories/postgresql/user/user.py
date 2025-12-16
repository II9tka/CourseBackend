import re

from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.models import UserLoginSchema
from api.v1.user.models import CreateUserSchema, UserSchema
from infrastructure.databases.postgresql.models import User
from infrastructure.repositories.postgresql.user.exceptions import UserIsExist


class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CreateUserSchema) -> UserSchema:
        user = User(
            username=payload.username,
            full_name=payload.full_name,
            password=payload.password,
            biography=payload.biography,
            email=payload.email,
        )
        self._session.add(user)
        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(',')]
            values = [val.strip() for val in match.group(2).split(',')]

            raise UserIsExist(field=columns[0], value=values[0])
        schema = UserSchema(
            id=user.id,
            full_name=user.full_name,
            biography=user.biography,
            email=user.email,
            username=user.username,
        )
        return schema

    async def is_exists(self, schema: UserLoginSchema) -> bool:
        query = select(User).where(and_(User.password==schema.password, User.username==schema.username))
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return bool(user)