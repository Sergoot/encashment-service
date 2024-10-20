import random
from fastapi import APIRouter

from src.atm.models import AtmModel

atm_router = APIRouter(
    prefix="/atm",
    tags=["Банкоматы"]
)


@atm_router.get("/")
async def get_atm_in_moscow() -> list[AtmModel]:
    """ Эндпоинт для получения всех банкоматов Москвы """
    # north = (55.909185, 37.591617)
    # south = (55.575342, 37.601765)
    # west = (55.753904, 37.844768)
    # east = (55.764181, 37.372128)

    return [
        AtmModel(
            id=i,
            lat=55 + random.randint(753904, 909185) / 1000000,
            long=37 + random.randint(372128, 844768) / 1000000,
            balance=random.randint(0, 1000000)
        ) for i in range(1000)
    ]
