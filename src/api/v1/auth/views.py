from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from infrastructure.repositories.postgresql.user.exceptions import UserNotFound
from usecase.create_token.abstract import AbstractCreateTokenUseCase
from usecase.refresh_token.abstract import AbstractRefreshTokenUseCase

from .dependencies import create_token_use_case, refresh_token_use_case
from .models import UserLoginSchema, TokenSchema, RefreshTokenSchema

router = APIRouter(prefix='/auth')


@router.post("/token", response_model=TokenSchema)
async def create_token(
    payload: UserLoginSchema,
    usecase: AbstractCreateTokenUseCase = Depends(create_token_use_case)
) -> JSONResponse:
    try:
        token = await usecase.execute(payload)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=token.model_dump(mode='json'))


@router.post("/token/refresh", response_model=TokenSchema)
async def refresh_token(
    payload: RefreshTokenSchema,
    usecase: AbstractRefreshTokenUseCase = Depends(refresh_token_use_case)
) -> JSONResponse:
    token = await usecase.execute(payload)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=token.model_dump(mode='json'))
