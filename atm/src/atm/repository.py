from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.atm.models import Atm
from src.atm.schemas import AtmCreate, AtmModel
from .utils import get_radius_range


class AtmRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, atm: AtmCreate) -> None:
        await self.db.execute(
            insert(Atm).values(
                osm_id=atm.osm_id,
                lat=atm.coords.lat, 
                long=atm.coords.long,
                money_current=atm.capacity.current,
                money_max=atm.capacity.max,
            )
        )
        await self.db.commit()
    
    async def get_atm_by_id(self, atm_id: int) -> Atm:
        res = await self.db.execute(
            select(Atm).where(Atm.id==atm_id)
        )
        return res.scalar_one_or_none()
    
    async def get_atms(self, limit: int = 10) -> list[Atm]:
        res = await self.db.execute(
            select(Atm).limit(limit=limit)
        )
        return res.scalars().all()

    
    async def get_atms_by_radius_to_lat_long(self, lat: float, long: float, radius: int = 100) -> list[Atm]:
        ranges = get_radius_range(lat=lat, long=long, radius=radius)
        res = await self.db.execute(
            select(Atm) \
            .where(Atm.long.between(ranges["long_min"], ranges["long_max"])) \
            .where(Atm.lat.between(ranges["lat_min"], ranges["lat_max"])) \
            .order_by(Atm.money_current)
        )
        return res.scalars().all()