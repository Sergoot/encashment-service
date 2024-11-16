import random
import csv

from src.atm.models import Atm
from src.atm.repository import AtmRepository
from src.atm.schemas import AtmCreate, AtmModel, Coords, Capacity, AtmCapacity

class AtmService:

    def __init__(self, atm_repository: AtmRepository):
        self.repo = atm_repository

    def generate_filling(self) -> AtmCapacity:

        MIN_MAX_CAPACITY = 2500  # Минимальная вместимость бункера
        MAX_MAX_CAPACITY = 3500  # Максимальная вместимость бункера
        MU_MAX = (MIN_MAX_CAPACITY + MAX_MAX_CAPACITY) / 2  # Среднее значение для нормального распределения
        SIGMA_MAX = (MAX_MAX_CAPACITY - MIN_MAX_CAPACITY) / 6  # Стандартное отклонение

        # Генерация максимальной вместимости бункеров по нормальному распределению в пределах диапазона
        max_capacity_bin1 = max(MIN_MAX_CAPACITY, min(random.gauss(MU_MAX, SIGMA_MAX), MAX_MAX_CAPACITY))
        max_capacity_bin2 = max(MIN_MAX_CAPACITY, min(random.gauss(MU_MAX, SIGMA_MAX), MAX_MAX_CAPACITY))

        # Генерация текущей заполненности от 0 до max по нормальному распределению
        filling_bin1 = max(0, min(random.gauss(max_capacity_bin1 / 2, max_capacity_bin1 / 4), max_capacity_bin1))
        filling_bin2 = max(0, min(random.gauss(max_capacity_bin2 / 2, max_capacity_bin2 / 4), max_capacity_bin2))

        return AtmCapacity(
            money_in=Capacity(
                current=round(filling_bin1),
                max=round(max_capacity_bin1)
            ),
            money_out=Capacity(
                current=round(filling_bin2),
                max=round(max_capacity_bin2)
            )
        )
    
    async def fill_db_from_csv(self, filename: str = "ATMS.csv") -> bool:
        with open("src/files/" + filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            for ind, row in enumerate(reader):
                if ind == 0:
                    continue
                osm_id = int(row[0])
                long = float(row[1])
                lat = float(row[2])
                capacity = self.generate_filling()

                await self.repo.create(
                    atm=AtmCreate(
                        osm_id=osm_id,
                        coords=Coords(lat=lat, long=long),
                        capacity=capacity
                    )
                )
        return True
    
    async def get_atms(self, limit: int = 10) -> list[AtmModel]:
        atms: list[Atm] = await self.repo.get_atms(limit=limit)
        print(atms)       
        return [
            AtmModel(
                id=atm.id,
                osm_id=atm.osm_id,
                coords=Coords(lat=atm.lat, long=atm.long), 
                capacity=AtmCapacity(
                    money_in=Capacity(current=atm.money_in_current, max=atm.money_in_max),
                    money_out=Capacity(current=atm.money_out_current, max=atm.money_out_max)
                )
            ) for atm in atms
        ] 
    
    # def get_random_msc_coords(self) -> Coords:
    #     return Coords(
    #         lat = 55 + random.randint(753904, 909185) / 1000000,
    #         long = 37 + random.randint(372128, 844768) / 1000000
    #     )

    # def generate_atm_in_moscow(self):
    #     coords = self.get_random_msc_coords()
    #     capacity = self.generate_filling(latitude=coords.lat, longitude=coords.long)
    #     return {"coords": coords, "capacity": capacity}
