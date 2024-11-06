"""
ДАЖЕ НЕ ПЫТАЙСЯ ЭТО ЗАПУСКАТЬ
я потратил на просчет этого говна 35 часов на стационарном компе
не оптимизирован, но и скрипт разовый
"""
input('ты уверен???')

from scripts.Utils.PSQLutils.main import PSQL
from scripts.Utils.PSQLutils.config import TableNearest, ServerConf, TableATM, TableRoutes
import pandas as pd

from scripts.Utils.MapUtils.OSMUtils import OSMatms

atm_sql = PSQL(ServerConf, TableATM)
nn_sql = PSQL(ServerConf, TableNearest)

routes_sql = PSQL(ServerConf, TableRoutes)

atms = atm_sql.fetch_rows()
nn = nn_sql.fetch_rows()
atms = pd.DataFrame(atms, columns=['atm_osmid' , 'atm_lon', 'atm_lat' , 'operator', 'atm_in_mkad'])
nn = pd.DataFrame(nn, columns=['nn_osmid', 'atm_osmid' , 'nn_lon', 'nn_lat' , 'distance', 'nn_in_mkad'])

Merged_ATM_NN = pd.merge(atms, nn, on='atm_osmid')

Merged_ATM_NN = Merged_ATM_NN.sort_values(by='distance')
Merged_ATM_NN = Merged_ATM_NN[(Merged_ATM_NN['atm_in_mkad'] == True) & (Merged_ATM_NN['nn_in_mkad'] == True)]

#atms_in_use = list()
nn_all = set()
routes_in_db = routes_sql.fetch_rows()
routes_in_db = pd.DataFrame(routes_in_db, columns=TableRoutes.table_columns)
routes_in_db = set(routes_in_db['direction'])

count = 0
for index, row in Merged_ATM_NN.iterrows():
    count += 1
    #atms_in_use.append(row['atm_osmid'])
    nn_all.add(row['nn_osmid'])
    if count == 10:
        #break
        pass


routes_all = set()
for src in nn_all:
    for dst in nn_all:
        if src == dst:
            continue
        direction = f'{src}->{dst}'
        #direction = (src, dst)
        routes_all.add(direction)

routes_to_calculate = routes_all - routes_in_db

print('всего возможных маршрутов: ', len(routes_all))
print('маршрутов уже в БД: ', len(routes_in_db))
print('к вычислению: ',len(routes_to_calculate))


ox = OSMatms()
print('инициализация графа...')
ox.init_place_graph()
print('инициализация завершена')
count_done = 0
count_error = 0
for direction in routes_to_calculate:
    #print(direction)
    src, dst = direction.split('->')
    src = int(src)
    dst= int(dst)
    #direction = f'{src}->{dst}'
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








