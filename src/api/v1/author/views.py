from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.author import PostgreSQLAuthorRepository

from .models import AuthorSchema, CreateUpdateAuthorSchema

router = APIRouter(prefix='/authors')


@router.post("", response_model=AuthorSchema)
async def create_author(
    payload: CreateUpdateAuthorSchema,
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    repo = PostgreSQLAuthorRepository(session)
    author = await repo.create(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=author.model_dump())
