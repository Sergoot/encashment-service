import pandas as pd
from pandas import DataFrame
from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import (ServerConf,
                                            TableRoutes,
                                            TableRoutesToMAI,
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
        #self.workday_time = 14_400
        self.MAI_point = 266729320 #890858624 - нода кпп
        #self.MAI_point = None
        self.ATN_NN = None
        self.Routes = None
        self.Graph = None
        self.atm_nn_dict = None
        self.nn_atms_dict = None

        self._init_atm_nn()
        self._init_mapping_dicts()

        self.current_tcp_driver = 0 #этот параметр отвечает за тип нынешнего решения ТСП
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

        for _, row in self.Routes.iterrows():
            self.Graph.add_edge(
                int(row['src']),  # начальный узел
                int(row['dst']),  # конечный узел
                travel_time=row['time'],  # время перемещения как вес
                travel_distance=row['distance'],  # общая дистанция как дополнительный вес
                nodes=row['nodes'] #ноды osmid от src до dst
            )

        # добавление в графф самопетлей
        for node in self.Graph.nodes:
            self.Graph.add_edge(
                node,
                node,
                travel_time=0,
                travel_distance=0,
                nodes=[]
            )

    def _init_TSP_driver(self):

        self.tsp = TSP(self.Graph, start_point=self.MAI_point, end_point=self.MAI_point, debug=True)

        self.tsp_drivers = [
            self.tsp.TSP_soltion_DAVID_2,
            #self.tsp.TSP_solution_GPT,
            #self.tsp.TSP_solution_GPT,
            self.tsp.TSP_soltion_DAVID_2,
            ]
        self.tsp_drivers_kwargs = [
            #{},
            {'initial_temperature': 20000, 'cooling_rate': 0.999}, #это для первичной обработки по tsp gpt
            {'initial_temperature': 10000, 'cooling_rate': 0.995}
        ]

    def init_david_david(self):
        self.tsp_drivers = [
            self.tsp.TSP_soltion_DAVID_2,
            self.tsp.TSP_soltion_DAVID_2,
        ]
        self.tsp_drivers_kwargs = [
            {},
            {}
        ]

    def init_david_gpt(self):
        self.tsp_drivers = [
            self.tsp.TSP_soltion_DAVID_2,
            self.tsp.TSP_solution_GPT,
        ]
        self.tsp_drivers_kwargs = [
            {},
            {'initial_temperature': 10000, 'cooling_rate': 0.995}
        ]

    def init_gpt_david(self):
        self.tsp_drivers = [
            self.tsp.TSP_solution_GPT,
            self.tsp.TSP_soltion_DAVID_2,
        ]
        self.tsp_drivers_kwargs = [
            {'initial_temperature': 20000, 'cooling_rate': 0.999},
            {}
        ]
    def init_gpt_gpt(self):
        self.tsp_drivers = [
            self.tsp.TSP_solution_GPT,
            self.tsp.TSP_solution_GPT,
        ]
        self.tsp_drivers_kwargs = [
            {'initial_temperature': 20000, 'cooling_rate': 0.999},
            {'initial_temperature': 10000, 'cooling_rate': 0.995}
        ]
    def init_gpt(self):
        self.tsp_drivers = [
            self.tsp.TSP_solution_GPT,
        ]
        self.tsp_drivers_kwargs = [
            {'initial_temperature': 10000, 'cooling_rate': 0.995},
        ]
    def init_david(self):
        self.tsp_drivers = [
            self.tsp.TSP_soltion_DAVID_2,
        ]
        self.tsp_drivers_kwargs = [
            {},
        ]

    def init_david(self):
        self.tsp_drivers = [
            self.tsp.TSP_soltion_DAVID_2,
        ]
        self.tsp_drivers_kwargs = [
            {},
        ]

    def init_david_gpt_david(self):
        self.tsp_drivers = [
            self.tsp.TSP_soltion_DAVID_2,
            self.tsp.TSP_solution_GPT,
            self.tsp.TSP_soltion_DAVID_2
        ]
        self.tsp_drivers_kwargs = [
            {},
            {'initial_temperature': 20000, 'cooling_rate': 0.999},
            {}
        ]


    def TSP_driver(self, points):
        route, route_time, route_distance = self.tsp_drivers[self.current_tcp_driver](
            points,
            **self.tsp_drivers_kwargs[self.current_tcp_driver]
        )
        return route, route_time, route_distance


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

    def atms_to_nns(self, atms:list[int])->list[int]:
        output_nn = list()
        for atm in atms:
            nn = self.atm_nn_dict[atm]
            output_nn.append(nn)
        return output_nn


    def get_ATMs_via_NN(self, nn_osmid) -> list:
        if not isinstance(self.ATN_NN, DataFrame):
            raise Exception('Таблица банкоматов/обочин не инициализированна')
        try:
            return self.nn_atms_dict[nn_osmid]
        except Exception as e:
            raise Exception('Обочина не инициализирован')


    def get_route_via_atms(self, atms:list[int]):
        nns = list()
        for atm in atms:
            nns.append(self.get_NN_via_ATM(atm))
        route, route_time, route_distance = self.get_route_via_nns(nns)
        return route, route_time, route_distance

    def get_route_via_nns(self, nns:list[int])->(list[int],int,int):
        nns = list(filter(lambda a: a != self.MAI_point, nns)) #по большому счету костыль, тк в иногда
        #в маршрут под вычисление может попасть стартовая точка
        def remove_duplicates(arr):
            seen = set()
            result = []
            for item in arr:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            return result
        nns = remove_duplicates(nns)
        if not isinstance(self.Graph, DiGraph):
            raise Exception('Граф не инициализирован')
        if len(set(nns)) != len(nns):
            raise Exception('Есть повторяющиеся ноды')

        route, route_time, route_distance = self.TSP_driver(nns)
        return route, route_time, route_distance

    def sort_atms_via_route(self, atms, route):
        output = list()
        for node in route:
            if node == self.MAI_point:
                continue #костыль, тк я не могу сопоставить стартовую точку и какой либо банкомат, в бд этого тупо нет
            atms_in_node = self.nn_atms_dict[node]
            for atm in atms_in_node:
                if atm in atms: #важное условие, чтобы не выгружать все подряд банкоматы из ноды
                    output.append(atm)
        return output


    def OLD_calculate_ensemble_of_routes_OLD(self, atms:list[int] , sort_before=True):
        if len(set(atms)) != len(atms):
            raise Exception('Есть повторяющиеся банкоматы')
        #предварительная сортировка атмов для составления оптимального маршрута

        if sort_before:
            self.current_tcp_driver = 0
            optimal_route, _, _ = self.get_route_via_atms(atms)
            atms = self.sort_atms_via_route(atms, optimal_route)

        self.current_tcp_driver = 1

        output = list()
        current_car = 1

        current_atms = list()
        current_route = list()
        current_time = 0
        current_distance = 0

        new_atms = list()

        count = 0
        last_atm = atms[-1]
        for atm in atms:
            count += 1
            new_atms.append(atm)

            new_route, route_time, route_distance = self.get_route_via_atms(new_atms)
            new_time = len(new_atms) * self.atm_time + route_time
            new_distance = route_distance

            if new_time <= self.workday_time:
                current_atms = new_atms.copy()
                current_route = new_route
                current_time = new_time
                current_distance = new_distance
            if new_time > self.workday_time or atm == last_atm:
                sorted_atms = self.sort_atms_via_route(
                    current_atms.copy(),
                    current_route.copy()[1:-1])
                output.append({
                    'car_id': current_car,
                    'atms': sorted_atms,
                    'route': current_route.copy(),
                    'route_time':current_time,
                    'route_distance':current_distance
                })
                current_car += 1
                current_atms = list()
                current_route = list()
                current_time = 0
                new_atms = list()
                new_atms.append(atm)

        return output

    def calculate_ensemble_of_routes(self, atms:list[int]):

        if len(set(atms)) != len(atms):
            raise Exception('Есть повторяющиеся банкоматы')

        #конвертирование АТМов в НН
        nns_to_calc = self.atms_to_nns(atms)
        #первичная сортировка НН, может быть использовано несколько драйверов
        #все зависит от инициализированного массива драйверов
        #ПОСЛЕДНИЙ - БАЗОВЫЙ ПЕРЕД НЕПОСРЕДСТВЕННОЙ ВЫДАЧЕЙ, поэтому -1
        for index in range(len(self.tsp_drivers) - 1):

            #обьявляем каким методом делаем первичную сортировку
            self.current_tcp_driver = index
            nns_to_calc , _, _ = self.get_route_via_nns(nns_to_calc)  #непосредственно сортировка

            #убираем начальную и конечную ноду ЕСЛИ это маевник
            #условие полукостльные тк не хочется контролировать возвращает ли конкретный драйвер
            if nns_to_calc[0] == self.MAI_point:
                nns_to_calc = nns_to_calc[1:]
            if nns_to_calc[-1] == self.MAI_point:
                nns_to_calc = nns_to_calc[:-1]


        #ставим базовый драйвер, тот что последний в инициализированном массиве драйверов
        self.current_tcp_driver = len(self.tsp_drivers) - 1
        #обьявление необходимых переменных
        output = list()
        current_car = 1
        current_nns = list() #здесь хранятся
        current_route = list()
        current_time = 0
        current_distance = 0
        count = 0
        #перебор всех NN
        for nn in nns_to_calc:
            #добавляем NN к текущим
            current_nns.append(nn)

            #просчет маршрута, времени и тд
            new_route, route_time, route_distance = self.get_route_via_nns(current_nns)
            current_atms = self.sort_atms_via_route(atms, current_route)
            new_time = len(current_atms) * self.atm_time + route_time
            new_distance = route_distance

            #если мы укладываемся в рабочий день с новым маршрутом
            if new_time <= self.workday_time:
                #делаем его основным
                current_route = new_route
                current_time = new_time
                current_distance = new_distance

            #если время вышло, или нода последняя, записать в output
            if new_time > self.workday_time or nn == nns_to_calc[-1]:
                #print(current_car, new_time > self.workday_time, nn == nns_to_calc[-1], nn , nns_to_calc[-1])
                #print(nns_to_calc)

                output.append({
                    'car_id': current_car,
                    'atms': current_atms, #сортируем АТМЫ по построенному маршруту
                    'route': current_route,
                    'route_time':current_time,
                    'route_distance':current_distance
                })
                #если нода не последняя обновляем по новой текущие параметры
                #это важно делать, иначе нынешняя NN теряется

                current_car += 1
                current_nns = [nn]
                current_route, current_time, current_distance = self.get_route_via_nns(current_nns)

                    #if current_time > self.workday_time:
                    #    raise Exception('Ты шиз? У тебя маршрут с ОДНОЙ нодой занял больше продолжительности дня')

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
    nns_total = set(atms['nn_osmid'])
    atms = list(atms['atm_osmid'])


    start = time()
    lol._init_routes()
    print('инициализация маршрутов из БД: ',time() - start)
    start = time()
    lol._init_graph()
    print('инициализация графа: ',time() - start)
    start = time()
    lol._init_TSP_driver()
    print('инициализация тсп: ', time() - start)


    start = time()
    print('все точки')

    test_total_atms = list()
    test_total_routes = list()
    test_car_ids = list()
    test_total_time = list()
    test_total_distance = list()
    lolkek = lol.calculate_ensemble_of_routes(atms)
    for kek in lolkek:
        test_total_atms += kek['atms']
        test_total_routes += kek['route']
        test_car_ids.append(kek['car_id'])
        test_total_time.append(kek['route_time'])
        test_total_distance.append(kek['route_distance'])
        print(kek['car_id'], kek['route'])
    print()
    print('всего задействовано машин:' , max(test_car_ids))
    print('просчет со всеми точками: ',time() - start)
    print('банкоматов в выводе:', len(test_total_atms), 'какие проебали:',set(atms) - set(test_total_atms))
    print('всего посещено НН:', len(set(test_total_routes)))
    print('проебано НН:', len(set(nns_total) - set(test_total_routes)) , set(nns_total) - set(test_total_routes))
    print()
    print('среднее время',sum(test_total_time)/max(test_car_ids), 'макс/мин', max(test_total_time), min(test_total_time), 'сумма', sum(test_total_time))
    print()
    print('средняя дистанция',sum(test_total_distance)/max(test_car_ids), 'макс/мин', max(test_total_distance), min(test_total_distance), 'сумма', sum(test_total_distance))

    #print(route)
    #start = time()
    #lol.get_route_via_atms(atms)
    #print('просчет маршрута для 1000 банкоматов шутки ради', time() - start)



if __name__ == '__main__':
    test()