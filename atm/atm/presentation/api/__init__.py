from fastapi import APIRouter

from .handlers import router


root_router = APIRouter()


root_router.include_router(router, prefix="/atms")
