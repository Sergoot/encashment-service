import pandas as pd
from pandas import DataFrame
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import (ServerConf,
                                            TableATM,
                                            TableNearest,
                                            TableRoutes,
                                            TableRoutesToMAI,
                                            TableAllowedATMs,
                                            TableATMAllowedNew)
from scripts.ATM_full_graph.TSP_solutions import TSP
import networkx as nx
from networkx import DiGraph

from time import time


class Algo:
    def __init__(self,
                 db_server_conf,
                 db_table_atm_nn,
                 db_table_routes,
                 db_table_routes_MAI
                 ):
        self.db_server_conf = db_server_conf
        self.db_table_atm_nn = db_table_atm_nn
        self.db_table_routes = db_table_routes
        self.db_table_routes_MAI = db_table_routes_MAI

        self.atm_time = 300 #5 минут на банкомат
        self.workday_time = 28_800 #рабочий день в секунах, 8 часов
        self.MAI_point = 266729320
        #self.MAI_point = None
        self.ATN_NN = None
        self.Routes = None
        self.Graph = None
        self.atm_nn_dict = None
        self.nn_atms_dict = None

        self._init_atm_nn()
        self._init_mapping_dicts()
        #self._init_routes()
        #self._init_graph()


    def _init_atm_nn(self):
        atm_nn_sql = PSQL(self.db_server_conf, self.db_table_atm_nn)
        self.ATN_NN = pd.DataFrame(atm_nn_sql.fetch_rows(), columns=self.db_table_atm_nn.table_columns)
        atm_nn_sql.close()

    def _init_mapping_dicts(self):
        if not isinstance(self.ATN_NN, DataFrame):
            raise Exception('Таблица банкоматов/обочин не инициализированна')

        self.atm_nn_dict = dict()
        self.nn_atms_dict = dict()
        for index, row in self.ATN_NN.iterrows():
            atm = row['atm_osmid']
            nn = row['nn_osmid']
            self.atm_nn_dict[atm] = nn

            if nn in self.nn_atms_dict:
                self.nn_atms_dict[nn].append(atm)
            else:
                self.nn_atms_dict[nn] = [atm]


    def _init_routes(self):
        routes_atms_sql = PSQL(self.db_server_conf, self.db_table_routes)
        routes_mai_sql = PSQL(self.db_server_conf, self.db_table_routes_MAI)

        routes_atms = pd.DataFrame(routes_atms_sql.fetch_rows(), columns=self.db_table_routes.table_columns)
        routes_mai = pd.DataFrame(routes_mai_sql.fetch_rows(), columns=self.db_table_routes_MAI.table_columns)

        self.Routes = pd.concat([routes_mai, routes_atms])

        routes_mai_sql.close()
        routes_atms_sql.close()

    def _init_graph(self):
        if not isinstance(self.Routes, DataFrame):
            raise Exception('Маршруты не инициализированны')
        self.Graph = nx.DiGraph()

        for _, row in self.Routes .iterrows():
            self.Graph.add_edge(
                int(row['src']),  # начальный узел
                int(row['dst']),  # конечный узел
                #path=row['direction'],  # путь или информация о пути
                travel_time=row['time'],  # время перемещения как вес
                total_distance=row['distance'],  # общая дистанция как дополнительный вес
                nodes=row['nodes']
            )

    def check_atms_is_init(self, atms):
        out = list()
        for atm in atms:
            if not atm in self.atm_nn_dict:
                out.append(atm)
        return out

    def get_NN_via_ATM(self, atm_osmid) -> int:
        if not isinstance(self.ATN_NN, DataFrame):
            raise Exception('Таблица банкоматов/обочин не инициализированна')
        try:
            return self.atm_nn_dict[atm_osmid]
        except Exception as e:
            raise Exception('Банкомат не инициализирован')


    def get_ATMs_via_NN(self, nn_osmid) -> list:
        if not isinstance(self.ATN_NN, DataFrame):
            raise Exception('Таблица банкоматов/обочин не инициализированна')
        try:
            return self.nn_atms_dict[nn_osmid]
        except Exception as e:
            raise Exception('Обочина не инициализирован')


    def get_route_via_atms(self, atms:list[int]):
        nns = set()
        for atm in atms:
            nns.add(self.get_NN_via_ATM(atm))
        route, route_time = self.get_route_via_nns(nns)
        return route, route_time

    def get_route_via_nns(self, nns:list[int]):
        if not isinstance(self.Graph, DiGraph):
            raise Exception('Граф не инициализирован')
        if len(set(nns)) != len(nns):
            raise Exception('Есть повторяющиеся ноды')
        tsp = TSP(self.Graph, nns, start_point=self.MAI_point, end_point=self.MAI_point, debug=True)
        route, route_time = tsp.TSP_solution_GPT()
        return route, route_time

    def get_route_via_atms_for_sort(self, atms:list[int]):
        nns = set()
        for atm in atms:
            nns.add(self.get_NN_via_ATM(atm))
        route, route_time = self.get_route_via_nns_for_sort(nns)
        return route, route_time


    def get_route_via_nns_for_sort(self, nns:list[int]):
        if not isinstance(self.Graph, DiGraph):
            #raise Exception('Граф не инициализирован')
            pass
        if len(set(nns)) != len(nns):
            raise Exception('Есть повторяющиеся ноды')
        tsp = TSP(self.Graph, nns, debug=True)
        route, route_time = tsp.TSP_solution_GPT(initial_temperature=20_000, cooling_rate=0.9999)
        return route, route_time

    def sort_atms_via_route(self, atms, route):
        output = list()
        for node in route:
            atms_in_node = self.nn_atms_dict[node]
            for atm in atms_in_node:
                if atm in atms:
                    output.append(atm)
        return output

    def first_sort(self , atms):
        optimal_route, _ = self.get_route_via_atms_for_sort(atms)
        output = self.sort_atms_via_route(atms, optimal_route)
        return output

    def calculate_ensemble_of_routes(self, atms:list[int] , sort_before=True):
        if len(set(atms)) != len(atms):
            raise Exception('Есть повторяющиеся банкоматы')
        #предварительная сортировка атмов для составления оптимального маршрута
        if sort_before:
            atms = self.first_sort(atms)
        output = list()
        current_car = 1

        current_atms = list()
        current_route = list()
        current_time = 0

        new_atms = list()

        count = 0
        last_atm = atms[-1]
        for atm in atms:
            count += 1
            new_atms.append(atm)
            new_route, route_time = self.get_route_via_atms(new_atms)
            new_time = len(new_atms) * self.atm_time + route_time

            if new_time <= self.workday_time:
                current_atms = new_atms.copy()
                current_route = new_route
                current_time = new_time
            if new_time > self.workday_time or atm == last_atm:
                sorted_atms = self.sort_atms_via_route(
                    current_atms.copy(),
                    current_route.copy()[1:-1])
                output.append({
                    'car_id': current_car,
                    'atms': sorted_atms,
                    'route': current_route.copy(),
                    'route_time':current_time
                })
                current_car += 1
                current_atms = list()
                current_route = list()
                current_time = 0
                new_atms = list()
                new_atms.append(atm)

        return output


def test():

    lol = Algo(
        db_server_conf=ServerConf,
        db_table_atm_nn=TableATMAllowedNew,
        db_table_routes=TableRoutes,
        db_table_routes_MAI=TableRoutesToMAI
    )


    atms_sql = PSQL(ServerConf, TableATMAllowedNew)
    atms = atms_sql.fetch_rows()
    atms = pd.DataFrame(atms, columns=TableATMAllowedNew.table_columns)
    atms = list(atms['atm_osmid'])

    start = time()
    lol._init_routes()
    print('инициализация маршрутов из БД: ',time() - start)
    start = time()
    lol._init_graph()
    print('инициализация графа: ',time() - start)


    start = time()

    print('1 точка')
    print(lol.calculate_ensemble_of_routes([408385048]))
    print('2 точки')
    print(lol.calculate_ensemble_of_routes([941766735, 938253590]))
    print('3 точки')
    print(lol.calculate_ensemble_of_routes([408385048, 938253590, 941766735]))

    print('просчет тестов выше: ',time() - start)

    start = time()
    print('все точки')

    test_total_atms = list()
    test_total_routes = list()
    test_car_ids = list()
    test_total_time = list()
    lolkek = lol.calculate_ensemble_of_routes(atms)
    for kek in lolkek:
        print(kek)
        test_total_atms += kek['atms']
        test_total_routes += kek['route']
        test_car_ids.append(kek['car_id'])
        test_total_time.append(kek['route_time'])

    print('просчет со всеми точками: ',time() - start)
    print(len(test_total_atms), set(atms) - set(test_total_atms))
    print(len(test_total_routes), len(set(test_total_routes)))
    print(sum(test_total_time)/max(test_car_ids))
    #print(route)
    start = time()
    lol.get_route_via_atms(atms)
    print('просчет маршрута для 1000 банкоматов шутки ради', time() - start)

if __name__ == '__main__':
    test()