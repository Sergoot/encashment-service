"""
ДАЖЕ НЕ ПЫТАЙСЯ ЭТО ЗАПУСКАТЬ
я потратил на просчет этого говна 35 часов на стационарном компе
не оптимизирован, но и скрипт разовый
"""
#input('ты уверен???')

from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import TableNearest, ServerConf, TableATM, TableRoutes2, TableAllowedNNs
import pandas as pd

from scripts.Utils.MapUtils.OSMUtils import OSMatms

routes_sql = PSQL(ServerConf, TableRoutes2)


allowed_nn = PSQL(ServerConf,TableAllowedNNs)
allowed_nn = allowed_nn.fetch_rows()
allowed_nn = pd.DataFrame(allowed_nn, columns=['osmid'])


#atms_in_use = list()
nn_all = list(allowed_nn['osmid'])

print('Инициализация БД с нынешними маршрутами')
routes_in_db_set = set()
routes_in_db = routes_sql.fetch_rows()
routes_in_db = pd.DataFrame(routes_in_db, columns=TableRoutes2.table_columns)
print('Инициализация завершена')

for index, row in routes_in_db.iterrows():
    direction = (row['src'],row['dst'])
    routes_in_db_set.add(direction)


routes_all = set()
for src in nn_all:
    for dst in nn_all:
        if src == dst:
            continue
        direction = (src,dst)
        #direction = (src, dst)
        routes_all.add(direction)


routes_to_calculate = routes_all - routes_in_db_set

print('всего возможных маршрутов: ', len(routes_all))
print('маршрутов уже в БД: ', len(routes_in_db_set))
print('к вычислению: ',len(routes_to_calculate))


ox = OSMatms()
print('инициализация графа...')
ox.init_place_graph()
print('инициализация завершена')
count_done = 0
count_error = 0
for src,dst in routes_to_calculate:
    #print(direction)
    src = int(src)
    dst= int(dst)
    try:
        nodes = ox.get_shortest_route(src, dst)
        time = ox.get_travel_time(nodes)
        distance = ox.get_total_distance(nodes)
        count_done += 1
    except:
        nodes = [0]
        time = 0
        distance = 0
        count_error += 1
        print(f'error {count_error}')

    routes_sql.insert_row(
        direction=direction,
        src=src,
        dst=dst,
        nodes=nodes,
        time=time,
        distance=distance
        )


    print(f'просчитано:{count_done}/{len(routes_to_calculate)}')








