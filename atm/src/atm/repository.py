from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.atm.models import Atm
from src.atm.schemas import AtmCreate, AtmModel


class AtmRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, atm: AtmCreate) -> None:
        await self.db.execute(
            insert(Atm).values(
                lat=atm.coords.lat, 
                long=atm.coords.long,
                money_in_current=atm.capacity.money_in.current,
                money_in_max=atm.capacity.money_in.max,
                money_out_current=atm.capacity.money_out.current,
                money_out_max=atm.capacity.money_out.max)
        )
        await self.db.commit()
    
    async def get_atms(self, limit: int = 10) -> list[AtmModel]:
        res = await self.db.execute(
            select(Atm).limit(limit=limit)
        )
        return res.scalars().all()