from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from infrastructure.repositories.postgresql.user.exceptions import UserIsExist
# from infrastructure.repositories.postgresql.author import PostgreSQLAuthorUnitOfWork
from usecase.create_user.abstract import AbstractCreateUserUseCase

from .dependencies import get_user_unit_of_work, create_user_use_case
from .models import CreateUserSchema, UserSchema

router = APIRouter(prefix='/users')


@router.post("", response_model=UserSchema)
async def create_user(
    payload: CreateUserSchema,
    usecase: AbstractCreateUserUseCase = Depends(create_user_use_case)
) -> JSONResponse:
    try:
        user = await usecase.execute(payload)
    except UserIsExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())


