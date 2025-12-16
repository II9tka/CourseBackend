from fastapi import APIRouter

from .views import router as user_router

router = APIRouter(tags=["User"])

router.include_router(user_router)
