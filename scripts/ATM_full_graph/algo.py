import pandas as pd
from pandas import DataFrame
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import (ServerConf,
                                            TableATM,
                                            TableNearest,
                                            TableRoutes,
                                            TableRoutesToMAI,
                                            TableAllowedATMs)
from scripts.ATM_full_graph.TSP_solutions import TSP
import networkx as nx
from networkx import DiGraph

from time import time


class Algo:
    def __init__(self,
                 db_server_conf,
                 db_table_atm,
                 db_table_nn,
                 db_table_routes,
                 db_table_routes_MAI
                 ):
        self.db_server_conf = db_server_conf
        self.db_table_atm = db_table_atm
        self.db_table_nn = db_table_nn
        self.db_table_routes = db_table_routes
        self.db_table_routes_MAI = db_table_routes_MAI

        self.atm_time = 300 #5 минут на банкомат
        self.workday_time = 28_800 #рабочий день в секунах, 8 часов
        self.MAI_point = 266729320
        #self.MAI_point = None
        self.ATMs = None
        self.NNs = None
        self.Routes = None
        self.Graph = None

        self._init_atms()
        self._init_nn()
        #self._init_routes()
        #self._init_graph()


    def _init_atms(self):
        atms_sql = PSQL(self.db_server_conf, self.db_table_atm)
        self.ATMs = pd.DataFrame(atms_sql.fetch_rows(), columns=self.db_table_atm.table_columns)

    def _init_nn(self):
        nn_sql = PSQL(self.db_server_conf, self.db_table_nn)
        self.NNs = pd.DataFrame(nn_sql.fetch_rows(), columns=self.db_table_nn.table_columns)

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

    def get_NN_via_ATM(self, atm_osmid) -> int:
        if not isinstance(self.NNs, DataFrame):
            raise Exception('Таблица обочин не инициализированна')
        df = self.NNs
        out = df.loc[df['atm_osmid'] == atm_osmid]
        if len(out) != 1:
            raise Exception(f'В таблице OSMID {atm_osmid} банкомата {len(out)} != 1')

        return list(out['osmid'])[0]

    def get_ATMs_via_NN(self, nn_osmid) -> list:
        if not isinstance(self.NNs, DataFrame):
            raise Exception('Таблица обочин не инициализированна')
        df = self.NNs
        out = df.loc[df['osmid'] == nn_osmid]

        if len(out) == 0:
            raise Exception('Банкоматов не найдено')

        return list(out['atm_osmid'])

    def get_route_via_atms(self, atms:list[int]):
        nns = set()
        for atm in atms:
            nns.add(self.get_NN_via_ATM(atm))

        route, time = self.get_route_via_nns(nns)

        return route, time

    def get_route_via_nns(self, nns:set[int]):
        if not isinstance(self.Graph, DiGraph):
            raise Exception('Граф не инициализирован')
        tsp = TSP(self.Graph, nns , start_point=self.MAI_point, end_point=self.MAI_point)
        route, time = tsp.TSP_solution_GPT()
        return route, time

    def _init_mapping_dict(self):


    def calculate_ensemble_of_routes(self, atms:list[int]):
        output = list()
        current_car = 1

        current_atms = list()
        current_route = list()
        current_time = 0

        new_atms = list()
        new_route = list()
        new_time = 0
        count = 0
        last_atm = atms[-1]
        # в будущем надо входящий поток АТМов сортировать по TSP
        # то есть сначала просчитывать ОБЩИЙ самый оптимальный маршрут
        # а потом дробить его по машинкам
        for atm in atms:
            #print(count, len(atms))
            count += 1
            new_atms.append(atm)
            new_route, route_time = self.get_route_via_atms(new_atms)
            new_time = len(new_atms) * self.atm_time + route_time

            if new_time <= self.workday_time:
                current_atms = new_atms.copy()
                current_route = new_route
                current_time = new_time
            if new_time > self.workday_time or atm == last_atm:
                output.append({
                    'car_id': current_car,
                    'atms': current_atms.copy(),
                    'route': current_route.copy(),
                    'route_time':current_time
                })
                current_car += 1
                current_atms = list()
                current_route = list()
                current_time = 0

                new_atms = list()
                new_route = list()
                new_time = 0

                new_atms.append(atm)
                new_route, route_time = self.get_route_via_atms(new_atms)
                new_time = len(new_atms) * self.atm_time + route_time
        return output









lol = Algo(
    db_server_conf=ServerConf,
    db_table_atm=TableATM,
    db_table_nn=TableNearest,
    db_table_routes=TableRoutes,
    db_table_routes_MAI=TableRoutesToMAI
)
#print(lol.get_NN_via_ATM(408385048))
#(lol.get_ATMs_via_NN(1107533819))
#print(lol.get_NN_via_ATM(656132952))

start = time()
lol._init_routes()
print('инициализация маршрутов из БД: ',time() - start)
start = time()
lol._init_graph()
print('инициализация графа: ',time() - start)




atms_sql = PSQL(ServerConf, TableAllowedATMs)
atms = atms_sql.fetch_rows()
atms = pd.DataFrame(atms, columns=TableAllowedATMs.table_columns)
atms = list(atms['osmid'])

start = time()

print('1 точка')
print(lol.calculate_ensemble_of_routes([408385048]))
print('2 точки')
print(lol.calculate_ensemble_of_routes([408385048, 938253590]))
print('3 точки')
print(lol.calculate_ensemble_of_routes([408385048, 938253590, 941766735]))

print('просчет тестов выше: ',time() - start)

start = time()
print('все точки')

test_total_atms = list()
test_total_routes = list()
lolkek = lol.calculate_ensemble_of_routes(atms)
for kek in lolkek:
    print(kek)
    test_total_atms += kek['atms']
    test_total_routes += kek['route']
print('просчет со всеми точками: ',time() - start)
print(len(test_total_atms), set(atms) - set(test_total_atms))
print(len(test_total_routes), len(set(test_total_routes)))

#print(route)
start = time()
lol.get_route_via_atms(atms)
print('просчет маршрута для 1000 банкоматов шутки ради', time() - start)