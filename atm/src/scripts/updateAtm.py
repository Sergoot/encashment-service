import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from src.atm.models import Atm


async def update_atm_data(db: AsyncSession):
    # Получаем все банкоматы из базы данных
    result = await db.execute(select(Atm))
    atms = result.scalars().all()

    for atm in atms:
        # Увеличение priem_current с использованием распределения Гаусса в диапазоне от priem_current до priem_max
        priem_mu = (atm.priem_current + atm.priem_max) / 2  # Среднее значение в середине диапазона
        priem_sigma = (atm.priem_max - atm.priem_current) / 4  # Стандартное отклонение для контроля разброса
        priem_increment = random.gauss(priem_mu, priem_sigma)

        # Убедимся, что priem_current не превышает priem_max
        atm.priem_current = min(atm.priem_current + priem_increment, atm.priem_max)

        # Уменьшение vidacha_current с использованием распределения Гаусса в диапазоне от 0 до vidacha_current
        vidacha_mu = atm.vidacha_current / 2  # Среднее значение в середине диапазона
        vidacha_sigma = atm.vidacha_current / 4  # Стандартное отклонение для контроля разброса
        vidacha_decrement = random.gauss(vidacha_mu, vidacha_sigma)

        # Убедимся, что vidacha_current не меньше 0
        atm.vidacha_current = max(atm.vidacha_current - vidacha_decrement, 0)

        # Обновление данных в базе данных
        await db.execute(
            update(Atm)
            .where(Atm.id == atm.id)
            .values(
                priem_current=atm.priem_current,
                vidacha_current=atm.vidacha_current
            )
        )

    # Фиксируем изменения в базе данных
    await db.commit()
    print("Данные банкоматов успешно обновлены")