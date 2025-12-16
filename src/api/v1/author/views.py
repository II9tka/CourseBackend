from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from infrastructure.repositories.postgresql.author import PostgreSQLAuthorUnitOfWork
from usecase.create_author.abstract import AbstractCreateAuthorUseCase

from .dependencies import get_author_unit_of_work, create_author_use_case
from .models import AuthorSchema, CreateUpdateAuthorSchema, AuthorFilterSchema

router = APIRouter(prefix='/authors')


@router.post("", response_model=AuthorSchema)
async def create_author(
    payload: CreateUpdateAuthorSchema,
    usecase: AbstractCreateAuthorUseCase = Depends(create_author_use_case)
) -> JSONResponse:
    author = await usecase.execute(payload)
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
