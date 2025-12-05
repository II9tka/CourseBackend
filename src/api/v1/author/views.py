from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.session import get_async_session
from infrastructure.di.injection import get_author_unit_of_work
from infrastructure.repositories.postgresql.uow import PostgreSQLAuthorUnitOfWork

from .models import AuthorSchema, CreateUpdateAuthorSchema, AuthorFilterSchema

router = APIRouter(prefix='/authors')


@router.post("", response_model=AuthorSchema)
async def create_author(
    payload: CreateUpdateAuthorSchema,
    uow: PostgreSQLAuthorUnitOfWork = Depends(get_author_unit_of_work),
) -> JSONResponse:
    async with uow as uow_:
        author = await uow_.repository.create(payload)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=author.model_dump())


@router.get("/{author_id}", response_model=AuthorSchema)
async def get_author(
    author_id: int,
    uow: PostgreSQLAuthorUnitOfWork = Depends(get_author_unit_of_work),
) -> JSONResponse:
    async with uow as uow_:
        author = await uow_.repository.get(author_id)

    if author is None:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=author.model_dump(mode='json'))


@router.get("", response_model=AuthorSchema)
async def get_author_list(
    author_filters: AuthorFilterSchema = Depends(),
    uow: PostgreSQLAuthorUnitOfWork = Depends(get_author_unit_of_work),
) -> JSONResponse:
    async with uow as uow_:
        authors = await uow_.repository.list(**author_filters.model_dump(mode='python', exclude_none=True))

    return JSONResponse(status_code=status.HTTP_200_OK, content=[author.model_dump(mode='json') for author in authors])
