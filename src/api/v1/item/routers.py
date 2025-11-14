from fastapi import APIRouter

from .views import router as item_router

router = APIRouter(tags=["Item"])

router.include_router(item_router)
