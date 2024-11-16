import math
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.atm.models import Atm, AtmsDistances
from src.atm.schemas import AtmCreate, AtmModel


class AtmRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, atm: AtmCreate) -> None:
        await self.db.execute(
            insert(Atm).values(
                osm_id=atm.osm_id,
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
    
    def get_radius_range(self, lat: float, long: float, radius: int = 100):
        # Earth's radius in meters
        R = 6371000  # Radius of Earth in meters
        
        # Convert latitude and longitude to radians
        lat_rad = math.radians(lat)
        lon_rad = math.radians(long)
        
        # Calculate changes in latitude and longitude
        dlat = math.sqrt(1 / (R * math.cos(lat_rad))) * radius  # 100m in degrees
        dlon = math.sqrt(1 / R) * radius # 100m in degrees
        
        # Calculate new coordinates
        north_lat = lat + dlat
        south_lat = lat - dlat
        east_lon = long + dlon
        west_lon = long - dlon
        
        return {
            'lat_max': north_lat,
            'lat_min': south_lat,
            'long_max': east_lon,
            'long_min': west_lon
        }
    
    async def get_atms_by_radius_to_atm(self, atm_id: int, radius: int = 100):
        res = await self.db.execute(
            select(Atm) 
            .where(Atm.id.in_(
                select(AtmsDistances) \
                .where(AtmsDistances.atm1_id == atm_id) \
                .filter(AtmsDistances.distance <= radius) \
                .order_by(AtmsDistances.distance)
            ))
        )
        return res.scalars().all()
    
    async def get_atms_by_radius_to_lat_long(self, lat: float, long: float, radius: int = 100):
        ranges = self.get_radius_range(lat=lat, long=long)
        res = await self.db.execute(
            select(Atm) \
            .where(Atm.long.between(ranges["long_min"], ranges["long_max"])) \
            .where(Atm.lat.between(ranges["lat_min"], ranges["lat_max"])) \
            .order_by(Atm.money_out_current)
        )
        return res.scalars().all()