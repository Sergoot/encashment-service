from typing import Annotated

from sqlalchemy import select, update
from src.atm.repository import AtmRepository
from src.atm.models import Atm
from src.database import get_session
from src.atm.service import AtmService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.atm.schemas import AtmModel, BaseResponse, Capacity, ChangeAtmCapacity, Coords

atm_router = APIRouter(
    prefix="/atm",
    tags=["Банкоматы"]
)

@atm_router.get("")
async def get_atm_in_moscow(limit: int, db: Annotated[AsyncSession, Depends(get_session)]) -> list[AtmModel]:
    """ Эндпоинт для получения всех банкоматов Москвы """
    return await AtmService(atm_repository=AtmRepository(db=db)).get_atms(limit=limit)


@atm_router.post("")
async def fill_db(db: Annotated[AsyncSession, Depends(get_session)]) -> BaseResponse:
    """ Эндпоинт для заполнения бд из файла """
    res = await AtmService(atm_repository=AtmRepository(db=db)).fill_db_from_csv()
    if res:
        return BaseResponse(status=True, message="Success")
    raise HTTPException(status_code=400, detail="Failed")


@atm_router.get("/closest")
async def get_closest_atms_by_distance(radius: int, lat: float, long: float, db: Annotated[AsyncSession, Depends(get_session)])-> list[AtmModel]:
    return await AtmService(atm_repository=AtmRepository(db=db)).get_closest_atms_to_lat_long_by_radius(lat=lat, long=long, radius=radius)


@atm_router.get("/{atm_id}")
async def get_atm_by_id(atm_id: int, db: Annotated[AsyncSession, Depends(get_session)]) -> AtmModel:
    """ Эндпоинт для получения банкомата из бд """
    res: Atm = await AtmRepository(db=db).get_atm_by_id(atm_id=atm_id)
    if not res:
        raise HTTPException(status_code=404, detail="Not found")

    return AtmModel(
        id=res.id,
        osm_id=res.osm_id,
        coords=Coords(lat=res.lat, long=res.long),
        capacity=Capacity(current=res.money_current, max=res.money_max)
    )


@atm_router.patch("/{atm_id}")
async def change_atm_capacity(atm_id: int, data: ChangeAtmCapacity, db: Annotated[AsyncSession, Depends(get_session)]) -> BaseResponse:
    """ Эндпоинт для изменения наполненности банкомата """
    res: Atm = await AtmRepository(db=db).get_atm_by_id(atm_id=atm_id)
    if not res:
        raise HTTPException(status_code=404, detail="Not found")
    
    if data.money_current > res.money_max:
        raise HTTPException(status_code=400, detail="Value is bigger than max capacity atm {atm_id}")
    
    await db.execute(
        update(Atm).where(Atm.id == atm_id).values(
            money_current=data.money_current,
        )
    )
    await db.commit()
    return BaseResponse(status=True, message="Success")