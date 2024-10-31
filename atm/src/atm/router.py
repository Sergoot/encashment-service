from typing import Annotated

from sqlalchemy import insert, select, update
from src.atm.models import Atm
from src.database import get_session
from src.atm.Service import AtmService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.atm.schemas import AtmCapacity, AtmCreate, AtmModel, BaseResponse, Capacity, ChangeAtmCapacity, Coords

atm_router = APIRouter(
    prefix="/atm",
    tags=["Банкоматы"]
)

@atm_router.post("")
async def create_atm_in_moscow(atm: AtmCreate, db: Annotated[AsyncSession, Depends(get_session)]) -> BaseResponse:
    res = await db.execute(
        insert(Atm).values(
            lat=atm.coords.lat,
            long=atm.coords.long,
            priem_current=atm.capacity.priem.current,
            priem_max=atm.capacity.priem.max,
            vidacha_current=atm.capacity.vidacha.current,
            vidacha_max=atm.capacity.vidacha.max
        )
        .returning(Atm.id)
    )
    await db.commit()
    return BaseResponse(status=True, message=f"Created ATM with id = {res.scalar_one_or_none()}")


@atm_router.get("")
async def get_atm_in_moscow(limit: int = 100) -> list[AtmModel]:
    """ Эндпоинт для получения всех банкоматов Москвы """
    return [
        AtmModel(id=i, **AtmService().generate_atm_in_moscow())
        for i in range(limit)
    ]


@atm_router.get("/{atm_id}")
async def get_atm_by_id(atm_id: int, db: Annotated[AsyncSession, Depends(get_session)]):
    """ Эндпоинт для получения банкомата из бд """
    res = (await db.execute(select(Atm).where(Atm.id == atm_id))).scalar_one_or_none()

    return AtmModel(
        id=res.id,
        coords=Coords(lat=res.lat, long=res.long),
        capacity=AtmCapacity(
            priem=Capacity(current=res.priem_current, max=res.priem_max),
            vidacha=Capacity(current=res.vidacha_current, max=res.vidacha_max)
        )
    )


@atm_router.patch("")
async def change_atm_capacity(data: ChangeAtmCapacity, db: Annotated[AsyncSession, Depends(get_session)]) -> BaseResponse:
    """ Эндпоинт для изменения наполненности банкомата """
    res = (await db.execute(select(Atm).where(Atm.id == data.id))).scalar_one_or_none()
    if not res:
        return HTTPException(status_code=404, detail="Not found")
    
    await db.execute(
        update(Atm).where(Atm.id == data.id).values(
            priem_current=data.priem,
            vidacha_current=data.vidacha
        )
    )
    await db.commit()
    return BaseResponse(status=True, message="Success")