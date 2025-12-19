from typing import Annotated

from fastapi import status, APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from infrastructure.repositories.postgresql.user.exceptions import UserIsExist
from usecase.create_user.abstract import AbstractCreateUserUseCase

from .dependencies import create_user_use_case
from .models import CreateUserSchema, UserSchema

router = APIRouter(prefix='/users')

security_scheme = HTTPBearer(scheme_name="Bearer")



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


@router.get("/me", response_model=UserSchema)
async def get_user_me(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> JSONResponse:
    return
    # try:
    #     user = await usecase.execute(payload)
    # except UserIsExist as e:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())
