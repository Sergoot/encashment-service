import pandas as pd
from pandas import DataFrame
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import ServerConf, TableATM, TableNearest, TableRoutes
from scripts.ATM_full_graph.TSP_solutions import TSP
import networkx as nx
from networkx import DiGraph

from time import time



class Algo:
    def __init__(self,
                 db_server_conf,
                 db_table_atm,
                 db_table_nn,
                 db_table_routes
                 ):
        self.db_server_conf = db_server_conf
        self.db_table_atm = db_table_atm
        self.db_table_nn = db_table_nn
        self.db_table_routes = db_table_routes

        self.atm_time = 300 #5 минут на банкомат

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
        routes_sql = PSQL(self.db_server_conf, self.db_table_routes)
        self.Routes = pd.DataFrame(routes_sql.fetch_rows(), columns=self.db_table_routes.table_columns)
        #тут надо дописать append к таблице с маршрутами от/до опорной точки

    def _init_graph(self):
        if not isinstance(self.Routes, DataFrame):
            raise Exception('Маршруты не инициализированны')
        self.Graph = nx.DiGraph()

        for _, row in self.Routes .iterrows():
            self.Graph.add_edge(
                row['src'],  # начальный узел
                row['dst'],  # конечный узел
                path=row['direction'],  # путь или информация о пути
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
        nns = list()
        for atm in atms:
            nns.append(self.get_NN_via_ATM(atm))
        return self.get_route_via_nns(nns)

    def get_route_via_nns(self, nns:list[int]):
        if not isinstance(self.Graph, DiGraph):
            raise Exception('Граф не инициализирован')
        tsp = TSP(self.Graph, nns)
        route = tsp.TSP_solution_GPT()
        return route


lol = Algo(
    db_server_conf=ServerConf,
    db_table_atm=TableATM,
    db_table_nn=TableNearest,
    db_table_routes=TableRoutes
)
#print(lol.get_NN_via_ATM(408385048))
#(lol.get_ATMs_via_NN(1107533819))
#print(lol.get_NN_via_ATM(656132952))

start = time()
lol._init_routes()
print(time() - start)

start = time()
lol._init_graph()
print(time() - start)

atms = [408385048, 938253590, 941766735]
start = time()
route = lol.get_route_via_atms(atms)
print(time() - start)
print(route)
