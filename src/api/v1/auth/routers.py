from fastapi import APIRouter

from .views import router as token_router

router = APIRouter(tags=["Token"])

router.include_router(token_router)
