import random

class AtmService:

    def __init__(self):
        pass

    def generate_filling(self, latitude: float, longitude: float):

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

        return {
            "priem": {
                "current": round(filling_bin1),
                "max": round(max_capacity_bin1)
            },
            "vidacha": {
                "current": round(filling_bin2),
                "max": round(max_capacity_bin2)
            }
        }