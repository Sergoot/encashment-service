#from scripts.ATM_full_graph.test_create_graph import start

import math
import random
import networkx as nx
import pandas as pd

from scripts.Utils.PSQLutils.config import ServerConf,TableRoutes
from scripts.Utils.PSQLutils.main import PSQL
from networkx import DiGraph

class TSP:
    def __init__(self, graph:DiGraph, points:set[int], start_point=None, end_point=None, edge_key='travel_time'):
        self.graph = graph
        self.points = points
        self.start_point = start_point
        self.end_point = end_point
        self.edge_key = edge_key

        if self.start_point in self.points:
            raise 'Начальная точка в точках для посещения'
        if self.end_point in self.points:
            raise 'Конечная точка в точках для посещения'

        for point in self.points:
            if point not in self.graph.nodes:
                raise ValueError(f"Нода {point} отсутствует в графе.")

        if start_point not in graph.nodes and start_point:
            raise ValueError("Начальная нода отсутствует в графе.")

        if end_point not in graph.nodes and end_point:
            raise ValueError("Начальная нода отсутствует в графе.")

    def get_current_route(self, route):
        if self.start_point:
            route = [self.start_point] + route
        if self.end_point:
            route = route + [self.end_point]
        return route

    def calculate_route_length(self, route):
        """Вычисляет длину маршрута для данного порядка узлов."""
        total_length = 0
        for i in range(len(route) - 1):
            total_length += self.graph[route[i]][route[i + 1]][self.edge_key]
        return total_length

    def TSP_solution_GPT(self, initial_temperature=10000, cooling_rate=0.995, min_temperature=1):

        #создаем нынешний маршрут
        current_route = list(self.points)

        #шафлим, можно и без этого в целом
        random.shuffle(current_route)

        #создаем нынешний маршрут с точкой отправления и прибытия
        current_route_with_start_stop = self.get_current_route(current_route)

        #просчитываем первоначальную длинну маршрута
        current_length = self.calculate_route_length(current_route_with_start_stop)

        #записываем лучший маршрут/время
        best_route = current_route_with_start_stop.copy()
        best_length = current_length

        #берем начальную температуру
        temperature = initial_temperature

        while temperature > min_temperature:
            #считаем новый маршрут
            new_route = current_route.copy()
            #меняем 2 рандомные точки местами
            if len(new_route) >= 2:
                i, j = random.sample(range(len(self.points)),2)
                new_route[i], new_route[j] = new_route[j], new_route[i]

            #добавляем в новый маршрут start/stop
            new_route_with_start_stop = self.get_current_route(new_route)

            # Вычисляем длину нового маршрута
            new_length = self.calculate_route_length(new_route_with_start_stop)

            # Разница между новым и текущим решениями
            delta_length = new_length - current_length

            # Решение принимается, если оно лучше, или с определенной вероятностью, если хуже
            if delta_length < 0 or math.exp(-delta_length / temperature) > random.random():
                current_route = new_route
                current_length = new_length

                # Обновляем лучшее решение
                if new_length < best_length:
                    best_route = new_route_with_start_stop
                    best_length = new_length

            # Понижаем температуру
            temperature *= cooling_rate

        return best_route, best_length


def test():
    routes_sql = PSQL(ServerConf, TableRoutes)

    routes_in_db = routes_sql.fetch_rows()
    routes_df = pd.DataFrame(routes_in_db, columns=TableRoutes.table_columns)

    G = nx.DiGraph()
    table_columns = ['direction', 'src', 'dst', 'nodes', 'time', 'distance']


    for _, row in routes_df.iterrows():
        G.add_edge(
            row['src'],  # начальный узел
            row['dst'],  # конечный узел
            path=row['direction'],  # путь или информация о пути
            travel_time=row['time'],  # время перемещения как вес
            total_distance=row['distance'],  # общая дистанция как дополнительный вес
            nodes=row['nodes']
        )
    algos = TSP(G, list(G.nodes))
    out = algos.TSP_solution_GPT()
    print(out)

if __name__ == '__main__':
    test()