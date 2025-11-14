from typing import Annotated

from fastapi import status, APIRouter, Query
from fastapi.responses import JSONResponse, Response

from api.pydantic.models import Pagination

from .models import Item, ListItem

_db: dict[int, Item] = {}

router = APIRouter(prefix='/items')


@router.get("", response_model=ListItem)
async def list_item(pagination: Annotated[Pagination, Query()]):
    return JSONResponse(ListItem.paginate(pagination, _db), status_code=status.HTTP_200_OK)


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in _db:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(_db[item_id].model_dump(mode='json'), status_code=status.HTTP_200_OK)


@router.post("", response_model=Item)
async def create_item(payload: Item):
    if not _db.keys():
        key = 1
    else:
        key = list(_db.keys())[-1] + 1

    payload.id = key
    _db.update({key: payload})
    return JSONResponse(payload.model_dump(mode='json'), status_code=status.HTTP_201_CREATED)


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    if item_id in _db:
        del _db[item_id]

        return JSONResponse({}, status_code=status.HTTP_204_NO_CONTENT)

    return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in _db:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    _db[item_id] = item

    return JSONResponse(item.model_dump(mode='json'), status_code=status.HTTP_200_OK)
