from typing import Annotated

from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse

from api.pydantic.models import Pagination

from .models import Book, ListBook, Genre

_db: dict[int, Book] = {}

router = APIRouter(prefix='/books')


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    if book_id not in _db:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(_db[book_id].model_dump(mode='json'), status_code=status.HTTP_200_OK)


@router.post("", response_model=Book)
async def create_book(payload: Book):
    if not _db.keys():
        key = 1
    else:
        key = list(_db.keys())[-1] + 1

    payload.id = key
    _db.update({key: payload})
    return JSONResponse(payload.model_dump(mode='json'), status_code=status.HTTP_201_CREATED)


@router.get("", response_model=ListBook)
async def list_book(pagination: Annotated[Pagination, Depends()], genre: Genre):
    return JSONResponse(ListBook.paginate(pagination, _db, genre=genre), status_code=status.HTTP_200_OK)
