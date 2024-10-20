import random
from src.atm.service import AtmService
from fastapi import APIRouter

from src.atm.models import AtmModel

atm_router = APIRouter(
    prefix="/atm",
    tags=["Банкоматы"]
)


@atm_router.get("/")
async def get_atm_in_moscow(limit: int) -> list[AtmModel]:
    """ Эндпоинт для получения всех банкоматов Москвы """
    return [
        AtmModel(id=i, **AtmService().generate_atm_in_moscow())
        for i in range(limit)]
