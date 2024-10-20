from fastapi import APIRouter
from src.atm.router import atm_router

main_router = APIRouter(
    prefix="/api/v1"
)

main_router.include_router(atm_router)