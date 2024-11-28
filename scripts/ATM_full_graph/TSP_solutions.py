
import math
import random


import networkx as nx
import pandas as pd

from scripts.Utils.PSQLutils.config import ServerConf,TableRoutes
from scripts.Utils.PSQLutils.main import PSQL
from networkx import DiGraph



class TSP:
    def __init__(self, graph:DiGraph, start_point=None, end_point=None, edge_key='travel_time', debug = False):
        self.graph = graph
        self.start_point = start_point
        self.end_point = end_point
        self.edge_key = edge_key
        self.debug = debug
        #self.with_start_end = True


        if start_point not in graph.nodes and start_point:
            raise ValueError("Начальная нода отсутствует в графе.")

        if end_point not in graph.nodes and end_point:
            raise ValueError("Начальная нода отсутствует в графе.")

    def get_current_route(self, route):
        #if self.with_start_end:
        if self.start_point:
            route = [self.start_point] + route
        if self.end_point:
            route = route + [self.end_point]
        #    return route
        #else:
        return route

    def _calculate_route_length(self, route:list, key_:str):
        """Вычисляет длину маршрута для данного порядка узлов."""
        total_length = 0
        for i in range(len(route) - 1):
            total_length += self.graph[route[i]][route[i + 1]][key_]
        return total_length

    def calculate_time(self, route:list):
        key = 'travel_time'
        return self._calculate_route_length(route, key)

    def calculate_distance(self, route:list):
        key = 'travel_distance'
        return self._calculate_route_length(route, key)

    def TSP_solution_GPT(self,
                         points,
                         initial_temperature=10000,
                         cooling_rate=0.995,
                         min_temperature=1 ,
                         random_shuffle = False,
                         **useless_shit):
        
        points = points[:]
        

        #шафлим, можно и без этого в целом
        if random_shuffle:
            random.shuffle(points)

        #создаем нынешний маршрут с точкой отправления и прибытия
        current_route_with_start_stop = self.get_current_route(points)

        #просчитываем первоначальную длинну маршрута
        current_time = self.calculate_time(current_route_with_start_stop)

        #записываем лучший маршрут/время
        best_route = current_route_with_start_stop.copy()
        best_time = current_time
        start_time = best_time

        #берем начальную температуру
        temperature = initial_temperature

        while temperature > min_temperature:
            #считаем новый маршрут
            new_route = points.copy()
            #меняем 2 рандомные точки местами
            if len(new_route) >= 2:
                i, j = random.sample(range(len(points)),2)
                new_route[i], new_route[j] = new_route[j], new_route[i]

            #добавляем в новый маршрут start/stop
            new_route_with_start_stop = self.get_current_route(new_route)

            # Вычисляем длину нового маршрута
            new_length = self.calculate_time(new_route_with_start_stop)

            # Разница между новым и текущим решениями
            delta_length = new_length - current_time

            # Решение принимается, если оно лучше, или с определенной вероятностью, если хуже
            if delta_length < 0 or math.exp(-delta_length / temperature) > random.random():
                points = new_route
                current_time = new_length

                # Обновляем лучшее решение
                if new_length < best_time:
                    best_route = new_route_with_start_stop
                    best_time = new_length

            # Понижаем температуру
            temperature *= cooling_rate
        best_distance = self.calculate_distance(best_route)
        if start_time > best_time:
            pass
            #print(start_time, best_time)
        return best_route, best_time, best_distance

    def TSP_soltion_DAVID(self, points:list[int], **useless_shit):
        """
        алгоритм берет стартовую точку в качестве начальной и далее идет к ближайшей и так до конца
        :param points: точки маршрута
        :param useless_shit: свалка
        :return: лучший маршрут, время и дистанция
        """
        points = points.copy()
        current_node = self.start_point
        route = [current_node]

        while points:
            # Найти ближайшую точку из оставшихся
            neighbors = {neighbor: self.graph[current_node][neighbor][self.edge_key] for neighbor in points}

            # Выбрать ближайшего соседа
            next_node, travel_cost = min(neighbors.items(), key=lambda x: x[1])

            # Добавить узел в маршрут
            route.append(next_node)

            # Удалить посещенную точку из оставшихся
            points.remove(next_node)

            # Переход к следующему узлу
            current_node = next_node

        route.append(self.end_point)
        #if not self.with_start_end:
        #    route.remove(self.start_point)
        #    route.remove(self.end_point)

        total_time = self.calculate_time(route)
        total_distance = self.calculate_distance(route)
        return route, total_time, total_distance

    def TSP_solution_ROLLER_MOBSTER(self, points:list[int], **useless_shit):
        """
        алгоритм циклически сдвигает элементы входного массива и смотрит что из этого получается
        :param points: точки маршрута
        :param useless_shit: свалка
        :return: лучший маршрут, время и дистанция
        """
        #обьявляем нынешние параметры лучшими
        best_route = self.get_current_route(points)
        best_time = self.calculate_time(best_route)
        best_distance = self.calculate_distance(best_route)

        start_time = best_time

        #начинаем делать циклический сдвиг влево на 1 элемент
        for index in range(len(points) - 1):
            points = points[1:] + points[:1] #сам сдвиг

            #записываем нынешние характеристики пути
            current_route = self.get_current_route(points)
            current_time = self.calculate_time(current_route)
            current_distance = self.calculate_distance(current_route)

            #проверяем выигрыш по времени
            #если выиграли - теперь это наши лучшие результаты
            if current_time < best_time:
                best_route = current_route
                best_time = current_time
                best_distance = current_distance
        #вернуть лучшие результаты
        if start_time != best_time:
            pass
            #print(start_time, best_time)
        return best_route, best_time, best_distance

    def TSP_solution_NOTHING(self, points:list[int], **useless_shit):
        current_route = self.get_current_route(points)
        current_time = self.calculate_time(current_route)
        current_distance = self.calculate_distance(current_route)
        return current_route, current_time, current_distance






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

def test_2():
    pass

if __name__ == '__main__':
    2/0
    test()