from fastapi import APIRouter

from .views import router as book_router

router = APIRouter(tags=["Book"])

router.include_router(book_router)
