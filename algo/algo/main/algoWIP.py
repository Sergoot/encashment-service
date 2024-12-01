import numpy as np
import networkx as nx
import random
from itertools import combinations

# Моделируем банкоматы
class ATM:
    def __init__(self, atm_id, location, capacity_in, capacity_out, mean_in, std_in, mean_out, std_out):
        self.atm_id = atm_id
        self.location = location  # координаты на карте
        self.capacity_in = capacity_in  # объем бункера приема
        self.capacity_out = capacity_out  # объем бункера выдачи
        self.mean_in = mean_in  # среднее количество банкнот, принимаемых в день
        self.std_in = std_in  # стандартное отклонение для принимаемых банкнот
        self.mean_out = mean_out  # среднее количество банкнот, выдаваемых в день
        self.std_out = std_out  # стандартное отклонение для выдаваемых банкнот
        self.current_in = 0  # текущее количество в бункере приема
        self.current_out = capacity_out  # текущее количество в бункере выдачи


# Генерируем случайные банкоматы
def generate_atms(n):
    atms = []
    for i in range(n):
        atm = ATM(
            atm_id=i,
            location=(random.uniform(0, 100), random.uniform(0, 100)),
            capacity_in=random.randint(500, 2000),
            capacity_out=random.randint(500, 2000),
            mean_in=random.randint(50, 150),
            std_in=random.randint(5, 20),
            mean_out=random.randint(50, 150),
            std_out=random.randint(5, 20)
        )
        atms.append(atm)
    return atms


# Моделируем дорожную сеть
def generate_road_network(atms):
    G = nx.Graph()
    for atm1, atm2 in combinations(atms, 2):
        distance = np.linalg.norm(np.array(atm1.location) - np.array(atm2.location))
        time_mean = distance / 10
        time_std = time_mean * 0.1
        G.add_edge(atm1.atm_id, atm2.atm_id, mean_time=time_mean, std_time=time_std)
    return G


def should_visit(atm, days_ahead):
    # Прогнозируем количество банкнот через несколько дней
    forecast_in = atm.current_in + np.random.normal(atm.mean_in * days_ahead, atm.std_in * days_ahead)
    forecast_out = atm.current_out - np.random.normal(atm.mean_out * days_ahead, atm.std_out * days_ahead)

    # print(f"Банкомат {atm.atm_id}: forecast_in={forecast_in}, forecast_out={forecast_out}, "
    #       f"capacity_in={atm.capacity_in}, capacity_out={atm.capacity_out}")

    # Проверяем, нужно ли обслуживать банкомат
    return forecast_in >= atm.capacity_in * 0.8 or forecast_out <= atm.capacity_out * 0.2  # временно снижены пороги


# Генерация маршрута для инкассаторов
def generate_route(atms, road_network, days_ahead, max_work_hours=8):
    groups = {i: [] for i in range(5)}  # 5 групп инкассаторов
    total_time = 0

    # Определяем, какие банкоматы нуждаются в обслуживании
    for atm in atms:
        if should_visit(atm, days_ahead):
            # Выбираем ближайший банкомат к маршруту группы инкассаторов
            closest_group = min(groups, key=lambda x: len(groups[x]))
            groups[closest_group].append(atm.atm_id)

    # Рассчитываем кратчайший путь для каждой группы
    for group in groups:
        route = groups[group]  # Маршрут для текущей группы
        if len(route) > 1:
            # Находим кратчайший путь между всеми банкоматами группы
            shortest_route = nx.shortest_path(road_network, source=route[0], target=route[-1], weight='mean_time')
            total_time += sum([road_network[shortest_route[i]][shortest_route[i + 1]]['mean_time'] for i in
                               range(len(shortest_route) - 1)])

    # Проверка на превышение лимита рабочего времени
    if total_time > max_work_hours * 60:  # если превышает рабочие 8 часов
        return generate_route(atms, road_network, days_ahead - 1)

    return groups


# Пример использования
atms = generate_atms(1000)  # 1000 банкоматов
road_network = generate_road_network(atms)

# Построение маршрутов на 1 день вперед
routes = generate_route(atms, road_network, days_ahead=1)
print(routes)



import time

# Функция для замера времени работы алгоритма
def algorithm_run(atms, road_network, days_ahead):
    start_time = time.time()  # замер времени начала работы алгоритма
    routes = generate_route(atms, road_network, days_ahead)
    end_time = time.time()  # замер времени окончания работы
    execution_time = end_time - start_time  # время выполнения алгоритма
    return routes, execution_time

# Генерация банкоматов и дорожной сети для теста
atms = generate_atms(1000)  # 1000 банкоматов
road_network = generate_road_network(atms)

# Тестируем на один день вперед
routes_1_day, time_1_day = algorithm_run(atms, road_network, days_ahead=1)
print(f"Время выполнения алгоритма для 1 дня: {time_1_day:.2f} секунд")

# Тестируем на три дня вперед
routes_3_days, time_3_days = algorithm_run(atms, road_network, days_ahead=3)
print(f"Время выполнения алгоритма для 3 дней: {time_3_days:.2f} секунд")

# Тестируем на семь дней вперед
routes_7_days, time_7_days = algorithm_run(atms, road_network, days_ahead=7)
print(f"Время выполнения алгоритма для 7 дней: {time_7_days:.2f} секунд")

# Сравнение полученных данных по времени и маршрутам
print(f"Маршруты для 1 дня: {routes_1_day}")
print(f"Маршруты для 3 дней: {routes_3_days}")
print(f"Маршруты для 7 дней: {routes_7_days}")

