from fastapi import APIRouter

from api.v1.item import routers as item_router

# router = FastAPI(version="1.0")
router = APIRouter(prefix="/api/v1")
router.include_router(item_router.router)
