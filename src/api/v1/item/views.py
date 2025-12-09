from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from api.pydantic.models import Pagination

from domain.item.models import Item, ItemCreateDTO, ItemUpdateDTO
from domain.item.repository import AbstractItemRepository, ItemNotFoundError

from .dependencies import get_item_repo
from .models import ItemSchema, ItemListSchema, ItemCreateSchema, ItemUpdateSchema

router = APIRouter(prefix='/items')


@router.post("", response_model=ItemSchema)
def create_item(
    payload: ItemCreateSchema,
    repo: AbstractItemRepository = Depends(get_item_repo),
) -> JSONResponse:
    dto = ItemCreateDTO(
        title=payload.title,
        description=payload.description,
    )
    item = repo.create(dto)

    # доменная модель -> Pydantic -> dict
    item_schema = ItemSchema(
        id=item.id,
        title=item.title,
        description=item.description,
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item_schema.model_dump())


@router.get("/{item_id}", response_model=ItemSchema)
def get_item(
    item_id: int,
    repo: AbstractItemRepository = Depends(get_item_repo),
) -> JSONResponse:
    try:
        item = repo.get(item_id)
    except ItemNotFoundError as exc:
        # Представим, что тут логирование ошибки
        print(exc)
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)

    item_schema = ItemSchema(
        id=item.id,
        title=item.title,
        description=item.description,
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content=item_schema.model_dump())


@router.get("", response_model=ItemListSchema)
def list_items(
    pagination: Pagination = Depends(),
    repo: AbstractItemRepository = Depends(get_item_repo),
) -> JSONResponse:
    items = repo.list(limit=pagination.limit, offset=pagination.offset)

    content = [
        ItemListSchema(
            id=item.id,
            title=item.title
        ).model_dump()
        for item in items
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content,
    )


@router.patch("/{item_id}", )
def update_item(
    item_id: int,
    payload: ItemUpdateSchema,
    repo: AbstractItemRepository = Depends(get_item_repo),
) -> JSONResponse:
    dto = ItemUpdateDTO(
        title=payload.title,
        description=payload.description,
    )

    try:
        item = repo.update(item_id, dto)
    except ItemNotFoundError as exc:
        # Представим, что тут логирование ошибки
        print(exc)
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)

    item_schema = ItemSchema(
        id=item.id,
        title=item.title,
        description=item.description,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=item_schema.model_dump(),
    )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    item_id: int,
    repo: AbstractItemRepository = Depends(get_item_repo),
):
    try:
        repo.delete(item_id)
    except ItemNotFoundError as exc:
        # Представим, что тут логирование ошибки
        print(exc)
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
